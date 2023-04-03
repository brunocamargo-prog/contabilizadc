import discord
from datetime import datetime, timedelta
from pytz import timezone

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True
intents.messages = True

client = discord.Client(intents=intents)

# Armazenar o tempo de entrada do membro no canal de voz
entry_time = {}


@client.event
async def on_voice_state_update(member, before, after):
    # Definir fuso horário de Brasília
    br_tz = timezone('America/Sao_Paulo')

    # Converter tempo atual para o fuso horário de Brasília
    current_time = datetime.now(br_tz)

    if before.channel != after.channel:
        if after.channel is not None:
            # Entrou no canal de voz
            entry_time[member.id] = current_time
        else:
            # Saiu do canal de voz
            if member.id in entry_time:
                duration = current_time - entry_time[member.id]
                minutes, seconds = divmod(duration.total_seconds(), 60)
                avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
                embed = discord.Embed(
                    title=f"{member.display_name}", description=f"Horário de entrada: {entry_time[member.id].strftime('%H:%M:%S')}\nHorário de saída: {current_time.strftime('%H:%M:%S')}\nTempo em call: {int(minutes)} minutos e {int(seconds)} segundos", color=0x00ff00)
                embed.set_thumbnail(url=avatar_url)
                # Substitua CHANNEL_ID pelo ID do Canal de texto onde deseja registrar a log
                channel = client.get_channel(123456789)
                await channel.send(embed=embed)
                del entry_time[member.id]

client.run('TOKEN')  # Substitua o 'TOKEN' pelo o Token de Seu bot!
