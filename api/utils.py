def send_res(code: int, message: str) -> 'JSON':
  return { 'code': code, 'message': message }
