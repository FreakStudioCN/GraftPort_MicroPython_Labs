# Python env   : MicroPython v1.23.0
# -*- coding: utf-8 -*-        
# @Time    : 2025/9/10 下午4:32   
# @Author  : 李清水            
# @File    : sensor_task.py       
# @Description : 每 200ms 读取超声波模块的测距距离、三点均值滤波、根据距离设置 LED 占空比与蜂鸣器频率（可调映射），支持 DEBUG 输出
# @License : CC BY-NC 4.0

# ======================================== 导入相关模块 =========================================

import time

# ======================================== 全局变量 ============================================

# ======================================== 功能函数 ============================================

# ======================================== 自定义类 ============================================

class LoraTask:
    def __init__(self, pcf8574, ssd1306, hc14_tx, hc14_rx):
        """构造参数:
        lora: HC14_Lora 实例（须提供发送/接收方法，代码中做了兼容处理）
        pcf8574: PCF8574 实例（需暴露 port 或 read()）
        ssd1306: SSD1306_I2C 实例（fill/text/show 等方法）
        """
        self.pcf8574 = pcf8574
        self.ssd1306 = ssd1306
        self.hc14_tx = hc14_tx
        self.hc14_rx = hc14_rx

    def _update_tx_display(self, text):
        # 清除 TX 区再写入
        self.ssd1306.fill_rect(30, 40, 90, 10, 0)
        self.ssd1306.text(text, 30, 40)
        self.ssd1306.show()

    def _update_rx_display(self, text):
        # 清除 RX 区再写入
        self.ssd1306.fill_rect(30, 52, 90, 10, 0)
        self.ssd1306.text(text, 30, 52)
        self.ssd1306.show()

    # -------------------- 调度器要调用的 tick() --------------------
    def tick(self):

        tmp = list(bin(self.pcf8574.port))[2:]
        tmp.reverse()
        tmp = [i for i, b in enumerate(tmp) if b == '0']
        if tmp ==  []:
            tx_index = None
        else:
            tx_index = tmp[0]
        
        if tx_index is None:
            return
        self.hc14_tx.transparent_send(f'01{tx_index}'.encode())
        self._update_tx_display(chr(ord('a') + tx_index))
        time.sleep(0.2)
        resp = self.hc14_rx.transparent_recv(timeout_ms=500, quiet_ms=200)[1].decode('utf-8')
        if resp[:2] == '01':
            self._update_rx_display(chr(ord('a') + int(resp[2])))




        

# ======================================== 初始化配置 ==========================================

# ========================================  主程序  ===========================================