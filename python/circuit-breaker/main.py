import random
import time

class CircuitBreaker:
    def __init__(self, fail_max, reset_timeout):
        self.fail_max = fail_max
        self.reset_timeout = reset_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'

    def call(self, func, *args, **kwargs):
        # Se o estado estive ropen, avalia se o tempo de reset ja foi superado, 
        # em caso positivo faça um teste avaliando se o serviço/api já está no ar. 
        # Retornando sucesso volte o estado para CLOSED caso contrário permaneça como OPEN
        if self.state == 'OPEN':
            if time.time() - self.last_failure_time > self.reset_timeout:
                self.state = 'HALF-OPEN'
            else:
                raise Exception("Circuit is open")

        try:
            result = func(*args, **kwargs)
            self._reset()
            return result
        except Exception as e:
            self._record_failure()
            raise e

    def _record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.fail_max:
            self.state = 'OPEN'

    def _reset(self):
        self.failure_count = 0
        self.state = 'CLOSED'

# Exemplo de uso
def external_service():
    # Simulação de uma chamada externa que pode falhar em 50% das vezes
    if random.randint(0,100) < 50:
        raise Exception("Service failed")
    return "Success"

circuit_breaker = CircuitBreaker(fail_max=2, reset_timeout=10)

for _ in range(30):
    try:
        result = circuit_breaker.call(external_service)
        print("Chamada bem-sucedida:", result)
    except Exception as e:
        print(e)
    time.sleep(1)
