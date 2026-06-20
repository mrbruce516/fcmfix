import os
import adbutils

# 从环境变量中读取宿主机的 IP，如果没传则默认连容器本地
# 在 Mac/Windows Docker 中，'host.docker.internal' 可以直接解析到宿主机 IP
HOST_IP = os.getenv("ADB_HOST", "host.docker.internal")
HOST_PORT = int(os.getenv("ADB_PORT", 5037))

print(f"正在尝试连接宿主机的 ADB 服务 -> {HOST_IP}:{HOST_PORT}")

try:
    # 显式指定宿主机的 ADB Server 运行地址
    adb_client = adbutils.AdbClient(host=HOST_IP, port=HOST_PORT)
    devices = adb_client.device_list()

    if not devices:
        print("宿主机的 ADB 没找到任何已连接设备... (´；ω；`) ")
    else:
        # 使用该 client 实例去初始化设备控制
        device = adb_client.device(serial=devices[0].serial)
        print(f"成功对接宿主机上的无线设备: {device.prop.model}")
        
        key_name = "google_restric_info"
        current_value = device.shell(["settings", "get", "secure", key_name]).strip()
        print(f"当前 {key_name} 的值为: '{current_value}'")
        
        if current_value == "1":
            print("检测到值为 1，正在修改为 0...")
            device.shell(["settings", "put", "secure", key_name, "0"])
            
            new_value = device.shell(["settings", "get", "secure", key_name]).strip()
            print(f"🎉 fcm已修复，验证结果: '{new_value}'")
        else:
            print("fcm状态正常，无需修复✨")
            
except Exception as e:
    print(f"❌ 容器内访问宿主机 ADB 失败: {e}")