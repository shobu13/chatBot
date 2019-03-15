# -*- coding: utf-8  -*-

# A lire si vous faîtes une mise à jour et si vous avez ajouté ou modifié les commandes du bot :
# 1) Copiez vos commandes (pas les commandes par défaut) que vous avez créer dans votre ancienne version dans la nouvelle version.
# 2) Si vous avez modifié une commande de NextBot par défaut, supprimez la commande de la nouvelle version puis copiez le code de la commande de l'ancienne version dans la nouvelle version.

import asyncio, discord
import apiai
import ast

token = "NTUxMDI0MTk2NzM0NTUwMDUy.D20Ssw.7pxdlEHP7G_iIZuqX4LI5NWUaCg"  # Mettez dans cette variable le token du bot
trust = ["Utilisateur 1",
         "Utilisateur 2"]  # Mettez dans cette variable les utilisateurs pouvant utiliser les commandes restreintes
trust_roles = [""]
ranks = False

client = discord.Client()
ver = "1.5.0"
lang = "fr"

print("NextBot " + ver + " " + lang)

ai = apiai.ApiAI('217938794488436ab84f7df8e327c294')


def getDialog(text, id):
    print(text, id)
    request = ai.text_request()
    request.lang = 'fr_FR'
    request.query = text
    response = request.getresponse().read().decode('utf-8')
    request.session_id = id
    response = response.replace('\n', '').replace('false', 'False').replace('true', 'True')
    response = ast.literal_eval(response)
    try:
        return response['result']['fulfillment']['messages'][0]['speech']
    except:
        return "kewa ?"


@client.event
@asyncio.coroutine
def on_message(message):
    rep = text = msg = message.content
    rep2 = text2 = msg2 = rep.split()
    user = str(message.author)
    user_bot_client = str(client.user)
    user_bot = user_bot_client.split("#")[0]
    role_trusted = False
    pm = message.server is None
    if not pm:
        server_msg = str(message.channel.server)
        chan_msg = str(message.channel.name)
        for role_name in trust_roles:
            if ":" in role_name and role_name.split(":")[0] == server_msg:
                rank_role = discord.utils.get(message.server.roles, name=":".join(role_name.split(":")[1:]))
            else:
                rank_role = discord.utils.get(message.server.roles, name=role_name)
            if isinstance(rank_role, discord.role.Role) and rank_role.id in [r.id for r in message.author.roles]:
                role_trusted = True
    else:
        server_msg = user
        chan_msg = user
    trusted = user in trust or role_trusted
    try:
        command = rep2[0].lower()
        params = rep2[0:]
    except IndexError:
        command = ""
        params = ""

    print(user + " (" + server_msg + ") [" + chan_msg + "] : " + rep)
    if user != 'shobot#5794':
        yield from client.send_message(message.channel, getDialog(text, user))
    if ranks and not pm and user != user_bot_client:
        open("msgs_user_" + server_msg + ".txt", "a").close()
        msgs = open("msgs_user_" + server_msg + ".txt", "r")
        msgs_r = msgs.read()
        if user not in msgs_r or user != user_bot_client:
            with open("msgs_user_" + server_msg + ".txt", "a") as msgs_w:
                msgs_w.write(user + ":0\n")
            msgs.close()
            msgs = open("msgs_user_" + server_msg + ".txt", "r")
            msgs_r = msgs.read()
        msgs_user = msgs_r.split(user + ":")[1]
        msgs.close()
        user_msgs_n = int(msgs_user.split("\n")[0])
        user_msgs_n += 1
        msgs_r = msgs_r.replace(user + ":" + str(user_msgs_n - 1), user + ":" + str(user_msgs_n))
        with open("msgs_user_" + server_msg + ".txt", "w") as msgs:
            msgs.write(msgs_r)

    # Début des commandes
    if command == "!commandtest":  # Copiez ce code pour créer une commande
        yield from client.send_message(message.channel, "Texte à envoyer.")

    if command == "!ban" and trusted and not pm:  # Cette commande n'est pas utilisable en MP
        if "<@" in params[1] and ">" in params[
            1]:  # La variable params[1] est le premier paramètre entré par l'utilisateur. Si le premier paramètre est une mention
            id_user = message.server.get_member(
                params[1].replace("<@", "").replace(">", ""))  # l'ID de l'utilisateur de la mention est récupéré
        else:  # sinon
            id_user = message.server.get_member_named(params[1])  # le pseudo entré en premier paramètre est recherché
        try:
            yield from client.ban(id_user, int(params[
                                                   2]))  # bannissement de l'utilisateur avec l'ID de l'utilisateur avec le nombre de messages à effacer
        except IndexError:  # si le 2ème paramètre n'est pas mis (erreur)
            yield from client.ban(id_user,
                                  0)  # bannissement de l'utilisateur avec l'ID de l'utilisateur sans le nombre de messages à effacer

    if command == "!bing":  # Cette commande sert à rechercher sur Bing
        yield from client.send_message(message.channel, "https://www.bing.com/search?q=" + "+".join(params[
                                                                                                    1:]))  # "+".join(params[1:]) sert à séparer les paramètres de la commande par des + pour que l'URL de recherche soit accessible, par exemple, en tapant !bing test 2, le bot renverra https://www.bing.com/search?q=test+2

    if command == "!create_channel" and trusted and not pm:  # Cette commande sert à créer un channel sur le serveur, " ".join(params[1:]) est le nom du channel et " ".join() sert à mettre les mots de params[1:] qui est une partie de la liste params qui contient tous les mots du message (à part la commande qui est params[0]).
        yield from client.create_channel(message.server, " ".join(params[1:]))

    if command == "!create_channel_voice" and trusted and not pm:  # Cette commande sert à créer un channel vocal, voir la commande précédente.
        yield from client.create_channel(message.server, " ".join(params[1:]), type=discord.ChannelType.voice)

    if command == "!delete" and trusted and not pm:  # Cette commande sert à supprimer un message avec un ID.
        message_del = client.get_message(message.channel, params[1])
        yield from client.delete_message(message_del)

    if command == "!google":  # Voir la commande !bing
        yield from client.send_message(message.channel, "https://www.google.com/#q=" + "+".join(params[1:]))

    if command == "!invite":  # Cette commande sert à générer une invitation pour le serveur. Voir la commande !ban
        try:
            invite = yield from client.create_invite(message.channel, max_age=params[1])
        except IndexError:
            invite = yield from client.create_invite(message.channel)
        yield from client.send_message(message.channel, invite.url)  # Renvoie le lien de l'url de l'invitation

    if command == "!join_channel_voice" and trusted:  # Cette commande sert à joindre un channel vocal.
        yield from client.join_voice_channel(discord.utils.get(message.server.channels, name=" ".join(params[1:])))

    if command == "!kick" and trusted and not pm:  # Voir la commande !ban
        if "<@" in params[1] and ">" in params[1]:
            id_user = message.server.get_member(params[1].replace("<@", "").replace(">", ""))
        else:
            id_user = message.server.get_member_named(params[1])
        yield from client.kick(id_user)

    if command == "!music" and trusted:  # Cette commande sert à lire de la musique, la premier paramètre est l'id du channel et le second est l'URL de la musique.
        voice_chan = yield from client.join_voice_channel(discord.utils.get(message.server.channels, name=" ".join(
            params[1:len(params) - 1])))  # Cette ligne sert à joindre le channel vocal.
        music = yield from voice_chan.create_ytdl_player(params[-1])  # Cette ligne sert à obtenir la musique de l'URL.
        music.start()  # Cette ligne sert à diffuser la musique.

    if command == "!nick" and trusted and not pm:  # Ici, on a une commande qui change le nom du bot
        yield from client.change_nickname(client.user, " ".join(params[1:]))

    if (
            command == "!prune_members" or command == "!purge_members") and trusted and not pm:  # Cette commande sert à purger les membres inactifs.
        try:
            yield from client.prune_members(message.server, days=int(params[1]))
        except IndexError:  # params[1] est le nombre de jours depuis la dernière connexion des membres, si le paramètre n'est pas mis, le bot purgera les membres qui ne sont pas connectés depuis 30 jours
            yield from client.prune_members(message.server, days=30)

    if (
            command == "!purge" or command == "!clear") and trusted and not pm:  # Cette commande sert à effacer les messages, en tapant !purge 10, le bot supprimera les 10 derniers messages.
        yield from client.purge_from(message.channel, limit=int(params[
                                                                    1]))  # Cette ligne sert à supprimer les messages avec params[1] qui est le premier paramètre (le nombre de messages), il y a int(params[1]) car le paramètre doit être converti en un nombre.

    if (command == "!quit" or command == "!exit") and trusted:  # Cette commande sert à fermer le bot
        yield from client.close()

    if command == "!quit_channel_voice" and trusted:  # Cette commande sert à quitter un channel vocal.
        for voice_chan in client.voice_clients:
            if voice_chan.channel == discord.utils.get(message.server.channels,
                                                       name=" ".join(params[1:])) and voice_chan.is_connected():
                yield from voice_chan.disconnect()

    if (
            command == "!rename_channel" or command == "!nick_channel") and trusted and not pm:  # Ici, il y a une commande qui renomme le channel où le message est envoyé
        yield from client.edit_channel(message.channel, name=" ".join(params[1:]))

    if command == "!role_user_add" and trusted and not pm:  # Cette commande sert à ajouter un rôle à un utilisateur
        if "<@" in params[1] and ">" in params[1]:
            member = message.server.get_member(params[1].replace("<@", "").replace(">", ""))
        else:
            member = message.server.get_member_named(params[1])
        role = discord.utils.get(message.server.roles, name=" ".join(params[
                                                                     2:]))  # cette ligne sert à récupérer le rôle de l'utilisateur à ajouter, " ".join(params[2:]) est le nom du rôle
        yield from client.add_roles(member,
                                    role)  # cette ligne sert à appliquer l'ajout du rôle à l'utilisateur et member est l'identifiant de l'utilisateur et role est l'identifiant du rôle

    if command == "!role_user_remove" and trusted and not pm:  # Cette commande sert à retirer un rôle à un utilisateur
        if "<@" in params[1] and ">" in params[1]:
            member = message.server.get_member(params[1].replace("<@", "").replace(">", ""))
        else:
            member = message.server.get_member_named(params[1])
        role = discord.utils.get(message.server.roles, name=" ".join(params[2:]))
        yield from client.remove_roles(member,
                                       role)  # cette ligne sert à retirer le rôle d'un utilisateur, son fonctionnement est quasi-identique à part qu'elle fait l'inverse (elle retire le rôle au lieu de l'ajouter)

    if command == "!roles" and trusted and not pm:  # Cette commande sert à lister les rôles sur le serveur
        for role in message.server.roles:  # cette ligne est une boucle et sert à mettre dans la variable role la liste des rôles du serveur avec message.server.roles
            yield from client.send_message(message.channel, role.id + " : " + role.name)

    if command == "!unban" and trusted and not pm:  # Cette commande sert à débannir un utilisateur
        if "<@" in params[1] and ">" in params[1]:
            id_user = message.server.get_member(params[1].replace("<@", "").replace(">", ""))
        else:
            id_user = message.server.get_member_named(params[1])
        yield from client.unban(message.server,
                                id_user)  # pour débannir un utilisateur, il faut l'identifiant du serveur avec message.serveur et l'identifiant de l'utilisateur (voir !ban)

    if command == "!say" and trusted:  # Cette commande sert à envoyer un message sur un channel du serveur, le paramètre 1 doit être l'identifiant du channel et après, on doit mettre le message (exemple : !say 1234567890 Bonjour !)
        yield from client.send_message(client.get_channel(params[1]), " ".join(params[2:]))

    if command == "!say_user" and trusted:
        if params[2].lower() == params[2].upper():
            yield from client.send_message(client.get_server(params[1]).get_member(params[2]), " ".join(params[3:]))
        else:
            yield from client.send_message(client.get_server(params[1]).get_member_named(params[2]),
                                           " ".join(params[3:]))

    if command == "!status_game" and trusted:  # Cette commande sert à mettre que le client joue à un jeu, " ".join(params[1:]) est le nom du jeu.
        yield from client.change_presence(game=discord.Game(name=" ".join(params[1:])))

    if (
            command == "!topic" or command == "!topic_channel") and trusted and not pm:  # Ici, on a une commande qui change le sujet du channel où est tapée la commande
        yield from client.edit_channel(message.channel, topic=" ".join(params[1:]))

    if command == "!ver":  # Cette commande envoit la version du bot.
        yield from client.send_message(message.channel,
                                       "NextBot " + ver + " " + lang + " Discord.py " + discord.__version__)

    if command == "!viki" or command == "!vikidia":  # Cette commande sert à envoyer un lien vers un article de Vikidia.
        yield from client.send_message(message.channel,
                                       "https://" + params[1] + ".vikidia.org/wiki/" + "_".join(params[2:]))

    if command == "!wp" or command == "!wikipedia":  # Cette commande sert à envoyer un lien vers un article de Wikipédia.
        yield from client.send_message(message.channel,
                                       "https://" + params[1] + ".wikipedia.org/wiki/" + "_".join(params[2:]))

    if "il est cool " + user_bot.lower() in rep.lower():  # Ici, le bot peut répondre a des phrases, par exemple, en disant "Il est cool NextBot", le bot répondra "Merci du compliment, vous aussi vous êtes cool !".
        yield from client.send_message(message.channel, "Merci du compliment, vous aussi vous êtes cool ! :)")


# Fin des commandes

# A partir d'ici, vous pouvez personnaliser ce que fait le bot quand quelqu'un rejoint un serveur, quitte un serveur, etc...
@client.event
@asyncio.coroutine
def on_member_join(member):  # Fonction quand quelqu'un rejoint un serveur
    chan_name = "general"  # Nom du canal où le message est envoyé
    yield from client.send_message(
        discord.utils.get(client.get_all_channels(), server__name=str(member.server), name=chan_name),
        "Bienvenue <@" + str(
            member.id) + "> !")  # Envoit du message (member.server.default_channel est le channel par défaut du serveur)


@client.event
@asyncio.coroutine
def on_member_remove(member):  # Fonction quand quelqu'un quitte un serveur
    chan_name = "general"
    yield from client.send_message(
        discord.utils.get(client.get_all_channels(), server__name=str(member.server), name=chan_name),
        "<@" + str(member.id) + "> a quitté le serveur.")


@client.event
@asyncio.coroutine
def on_message_delete(message):  # Fonction quand quelqu'un supprime un message
    chan_name = "general"
    yield from client.send_message(
        discord.utils.get(client.get_all_channels(), server__name=str(message.server), name=chan_name),
        "Le message " + str(message.id) + " a été supprimé par <@" + str(message.author.id) + "> sur <#" + str(
            message.channel.id) + ">. Contenu : " + message.content)


@client.event
@asyncio.coroutine
def on_message_edit(before, after):  # Fonction quand quelqu'un modifie un message
    chan_name = "general"
    yield from client.send_message(
        discord.utils.get(client.get_all_channels(), server__name=str(after.server), name=chan_name),
        "Le message " + str(
            after.id) + " a été modifié de '" + before.content + "' à '" + after.content + "' par <@" + str(
            after.author.id) + ">.")


@client.event
@asyncio.coroutine
def on_reaction_add(reaction, user):  # Fonction quand quelqu'un ajoute une réaction
    chan_name = "general"
    yield from client.send_message(
        discord.utils.get(client.get_all_channels(), server__name=str(user.server), name=chan_name),
        "<@" + str(user.id) + "> a réagi avec " + str(reaction.emoji) + " au message " + str(reaction.message.id) + ".")


@client.event
@asyncio.coroutine
def on_reaction_remove(reaction, user):  # Fonction quand quelqu'un enlève une réaction
    chan_name = "general"
    yield from client.send_message(
        discord.utils.get(client.get_all_channels(), server__name=str(user.server), name=chan_name),
        "<@" + str(user.id) + "> a enlevé la réaction " + str(reaction.emoji) + " au message " + str(
            reaction.message.id) + ".")


# Vous pouvez voir les autres fonctions ici : http://discordpy.readthedocs.io/en/latest/api.html#event-reference

client.run(token)
