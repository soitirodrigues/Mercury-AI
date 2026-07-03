from datetime import datetime


class NewsProvider:

    def get_news(self):

        now = datetime.now().strftime("%d/%m/%Y %H:%M")

        news = [
            {
                "title": "Federal Reserve mantém expectativa de juros.",
                "source": "Reuters",
                "impact": "High",
                "currency": "USD",
                "time": now,
            },
            {
                "title": "Ouro sobe com aumento da demanda por ativos de proteção.",
                "source": "Bloomberg",
                "impact": "Medium",
                "currency": "XAU",
                "time": now,
            },
            {
                "title": "Petróleo recua após divulgação dos estoques americanos.",
                "source": "Investing",
                "impact": "Medium",
                "currency": "OIL",
                "time": now,
            },
        ]

        return news