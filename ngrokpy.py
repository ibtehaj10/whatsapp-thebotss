from pyngrok import ngrok
import pywabot
# Start ngrok when app is run
ngrok_tunnel = ngrok.connect(5000)
print('ngrok tunnel "http://localhost:5000" -> "http://' + ngrok_tunnel.public_url + '"')

@pywabot.before_first_request
def ngrok_url():
    print("Your app is publicly accessible at", ngrok_tunnel.public_url)



ngrok_url()