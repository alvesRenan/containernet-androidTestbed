FORWARD_PORTS = "sh -c '/root/port_forward.sh' & "

ANDROID_EMU_START = """sh -c 'emulator @android-22 -memory 512 -partition-size 512 -no-boot-anim -accel auto -no-window -camera-back none -camera-front none -nojni -no-cache -no-audio -qemu -vnc :2' &"""

MPOS_START = "sh -c 'java -jar mposplatform.jar' & "

def send_res(code: int, message: str) -> 'JSON':
  return { 'code': code, 'message': message }
