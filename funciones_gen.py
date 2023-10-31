
def get_emojis():
	conceptos_con_emojis = {
      "Captación": "💰",
      "Seguro de Vida": "👨‍👩‍👧‍👦🛡️",  # Representa una familia y un escudo
      "Portabilidad": "📲",
      "Seguro de Salud": "🏥🛡️",
      "Crédito de Nómina": "💳🧾",
      "Seguro de Auto": "🚗🛡️",
      "Seguro de Hogar": "🏡🛡️",
      "Fondos": "💰💼",
      "Pagarés": "📝",
      "Tarjeta de Crédito": "💳",
      "Crédito Hipotecario": "🏠🏦",
      "PPI": "💸",
      "Crédito de Auto": "🚗💳",
      "EFI": "💵",
      "ILC": "📈💳"
    }
	return conceptos_con_emojis

def assigne_emoj(string, emoj):
	string = string.replace('Credito','Crédito').replace('Pagares','Pagarés').replace('Captacion','Captación').replace('Nomina','Nómina')
	for con, em in emoj.items():
		mostrar = em + con
		string = string.replace(con,mostrar)
	return string
