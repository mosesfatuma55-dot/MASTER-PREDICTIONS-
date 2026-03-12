import requests
import os

# Hii inachukua Key yako siri kutoka GitHub Secrets
API_KEY = os.getenv('FOOTBALL_API_KEY')
headers = { 'X-Auth-Token': API_KEY }

def get_matches_and_update():
    # URL ya kuchukua mechi za leo
    url = "https://api.football-data.org/v4/matches"
    
    try:
        print("Inaanza kuchukua data kutoka API...")
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Hitilafu ya API: {response.status_code}")
            return

        data = response.json()
        matches = data.get('matches', [])
        
        match_html_rows = ""
        
        # Tunachakata mechi 10 za kwanza
        for m in matches[:10]:
            home_team = m['homeTeam']['name']
            away_team = m['awayTeam']['name']
            league = m['competition']['code'] if m.get('competition') else "INT"
            match_time = m['utcDate'][11:16] 
            
            # Logic rahisi ya Prediction
            prediction = "OV 1.5"
            if "Arsenal" in home_team or "Madrid" in home_team:
                prediction = "GG"

            # Muundo wa HTML
            match_html_rows += f"""
                <tr>
                    <td class="match-info">
                        <span class="league">{league}</span>
                        <span class="team-name">{home_team}</span>
                        <span class="team-name">{away_team}</span>
                    </td>
                    <td>
                        <div class="h2h-container">
                            <div class="h2h-column">
                                <span class="h2h-date">Auto</span>
                                <div class="h2h-item">-<br>-</div>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div class="pred-stack">
                            <div class="pred-opt">{prediction}</div>
                        </div>
                    </td>
                    <td><span class="time-box">{match_time}</span></td>
                </tr>
            """

        # Fungua na usome index.html
        with open("index.html", "r", encoding="utf-8") as f:
            html_content = f.read()

        # Badilisha placeholder na mechi mpya
        if "" in html_content:
            new_html = html_content.replace("", match_html_rows)
            
            # Hifadhi mabadiliko
            with open("index.html", "w", encoding="utf-8") as f:
                f.write(new_html)
            print("Hongera! Mechi zimesasishwa.")
        else:
            print("Kosa: Placeholder haijaonekana!")

    except Exception as e:
        print(f"Hitilafu: {e}")

if __name__ == "__main__":
    get_matches_and_update()
