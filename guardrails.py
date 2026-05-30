
class Guardrails:

    def sense_check(text):

        tags = ["customer query", "not a customer query", "malicious attack on agent"]

        return "customer query"