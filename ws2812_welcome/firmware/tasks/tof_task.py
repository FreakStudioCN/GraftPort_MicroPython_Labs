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

class TofTask:
    def __init__(self, tof, nm):
        """
        Args:
            imu (IMU): 陀螺仪对象（带 RecvData()）
            nm (NeopixelMatrix): LED 矩阵对象
        """
        self.tof = tof
        self.nm = nm
        self.i = 0
        self.text = "Welcome to GXCVU"
        self.pos = self.nm.width   # 从屏幕最右边开始滚动

    def tick(self):
        """每次调用由调度器执行"""
        self.tof.start()
        time.sleep(0.1)
        distance = self.tof.read()
        if distance > 2000:
            self.i += 1
            self.nm.fill(0)
            self.nm.show()
        else:
            self.nm.fill(self.nm.COLOR_RED)
            self.nm.text(self.text, self.pos, 0, self.nm.COLOR_BLUE)
            self.nm.show()

            self.pos -= 1
            text_length = len(self.text) * 8  # 假设每个字符宽度为 8 像素
            if self.pos < -text_length:
                self.pos = self.nm.width  # 从头开始滚动

                                
    def reset(self):
        """重置任务状态"""
        if self.i < 50:
            return
        self.i = 0
        self.pos = self.nm.width
        self.nm.fill(self.nm.COLOR_GREEN)
        self.nm.show()

        

# ======================================== 初始化配置 ==========================================

# ========================================  主程序  ===========================================