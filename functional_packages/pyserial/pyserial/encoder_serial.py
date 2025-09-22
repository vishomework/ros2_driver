import serial
import asyncio
import time
import threading
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('AsyncSerial')

class AsyncSerial_t:
    def __init__(self, port, baudrate, frame_length=64):
        self.port = port
        self.baudrate = baudrate
        self.frame_length = frame_length  # 定长接收的数据帧长度
        self._serial = None
        self._callback = None
        self._wait_time = 0.01
        self._loop = None
        self._thread = None
        self.data_queue = asyncio.Queue()
        self.running = False
        
        logger.info(f"Initializing AsyncSerial for {port} at {baudrate} baud, frame length: {frame_length}")

    async def _connect_serial(self):
        logger.info("Starting serial connection task")
        while self.running:
            if self._serial is None or not self._serial.is_open:
                try:
                    logger.info(f"Attempting to connect to {self.port}...")
                    self._serial = serial.Serial(
                        port=self.port,
                        baudrate=self.baudrate,
                        bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        timeout=0  # 非阻塞模式
                    )
                    logger.info(f"\033[92m[SUCCESS] Serial connected: {self.port}\033[0m")
                except serial.SerialException as e:
                    logger.error(f"\033[91m[ERROR] Could not connect to serial port {self.port}: {e}\033[0m")
                    await asyncio.sleep(1)
            else:
                await asyncio.sleep(1)

    def __del__(self):
        self.stop()
        if self._serial and self._serial.is_open:
            self._serial.close()
            logger.info("Serial port closed in destructor")

    def startListening(self, callback=None, wait_time=0.0001) -> None:
        logger.info("Starting serial listener")
        self._wait_time = wait_time
        self.running = True
        
        if callback:
            self._callback = callback
            logger.info("Callback function set")
        else:
            logger.warning("No callback function provided")
            
        if self._loop is None:
            self._loop = asyncio.new_event_loop()
            self._thread = threading.Thread(target=self._run_loop, daemon=True)
            self._thread.start()
            logger.info("Created new event loop and thread")

        asyncio.run_coroutine_threadsafe(self._connect_serial(), self._loop)
        asyncio.run_coroutine_threadsafe(self.__read(), self._loop)
        asyncio.run_coroutine_threadsafe(self.datahandle(), self._loop)
        logger.info("Started serial tasks")
        
    def stop(self):
        logger.info("Stopping serial listener")
        self.running = False
        if self._loop and self._loop.is_running():
            self._loop.call_soon_threadsafe(self._loop.stop)
        if self._thread:
            self._thread.join(timeout=1.0)
        
    async def __read(self):
        logger.info("Starting read task (fixed-length mode)")
        buffer = bytearray()  # 数据缓冲区
        
        while self.running:
            await asyncio.sleep(self._wait_time)
            
            if not self._serial or not self._serial.is_open:
                logger.warning("Serial not connected, skipping read")
                await asyncio.sleep(1)
                continue

            try:
                # 检查是否有数据可读
                available = self._serial.in_waiting
                if available > 0:
                    # 读取所有可用数据
                    data = self._serial.read(available)
                    buffer.extend(data)
                    
                    # 处理完整的数据帧
                    while len(buffer) >= self.frame_length:
                        # 提取一帧数据
                        frame = bytes(buffer[:self.frame_length])
                        # 移除已处理的数据
                        buffer = buffer[self.frame_length:]
                        
                        # 将完整帧放入队列
                        self.data_queue.put_nowait(frame)
                        logger.debug(f"Received frame: {frame.hex()}")
                    
            except Exception as e:
                logger.error(f"Error during read: {e}")
                try:
                    if self._serial:
                        self._serial.close()
                except Exception:
                    pass
                self._serial = None
                await asyncio.sleep(1)
                
    async def datahandle(self):
        logger.info("Starting data handling task")
        while self.running:
            try:
                frame = await asyncio.wait_for(self.data_queue.get(), timeout=1.0)
                
                if self._callback:
                    try:
                        self._callback(frame)
                    except Exception as e:
                        logger.error(f"\033[91m[ERROR] Callback error: {e}\033[0m")
                else:
                    logger.warning("No callback set, discarding data")
                    
            except asyncio.TimeoutError:
                # 超时没有数据是正常的
                pass
            except Exception as e:
                logger.error(f"Error in data handling: {e}")
            
    def write(self, input_data: bytes) -> None:
        if not self._serial or not self._serial.is_open:
            logger.error("\033[91m[ERROR] Cannot write, serial not connected.\033[0m")
            return

        try:
            logger.debug(f"Writing {len(input_data)} bytes: {input_data.hex()}")
            self._serial.write(input_data)
            self._serial.flush()  # 确保数据发送出去
            logger.debug("Write successful")
        except Exception as e:
            logger.error(f"\033[91m[ERROR] Serial error during write: {e}\033[0m")
            try:
                if self._serial:
                    self._serial.close()
            except Exception:
                pass
            self._serial = None
            
    def _run_loop(self):
        logger.info("Starting event loop in background thread")
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()

def main():
    serial = AsyncSerial_t("/dev/ttyUSB0", 115200, frame_length=8)
    
    def data_callback(frame):
        try:
            # 尝试解码为文本
            text = frame.decode('utf-8', errors='replace')
            print(f"Callback received text: {text}")
        except:
            # 显示十六进制格式
            hex_data = ' '.join([f'{b:02X}' for b in frame])
            print(f"Callback received (HEX): {hex_data}")
    
    serial.startListening(data_callback)
    
    counter = 0
    try:
        while True:
            test_data = f"TEST{counter:04d}".encode()
            serial.write(test_data)
            counter += 1
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        serial.stop()

if __name__ == '__main__':
    main()