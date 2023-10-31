# Discord bot import
import os
import glob
import ndjson
import discord

# My program import


class add_program:
    async def add_interaction(self, interaction, name, member, stream_site_url, x_url, number_interrupt):

        await interaction.response.defer()

        # 言語の確認
        file = str(interaction.guild.id) + ".ndjson"

        with open('./data/language_json/' + file) as f:
            read_data = ndjson.load(f)

        language = read_data[0]["language_mode"]

        # URL2つがURLであるかを確認する
        if stream_site_url[0:8] == 'https://':
            pass
        else:
            if language == "ja":
                embed=discord.Embed(title="エラー！", description=":x:入力された「stream_site_url」がURLではありません！\n入力された内容を確認してください。:x:", color=0xff0000)
            else:
                embed=discord.Embed(title="Error!", description=":x:The [stream_site_url] entered is not a URL! \nPlease check the information you have entered.:x:", color=0xff0000)

            await interaction.followup.send(embed=embed)            
            return
        
        if x_url[0:20] == 'https://twitter.com/' or x_url[0:14] == 'https://x.com/':
            pass
        else:
            if language == "ja":
                embed=discord.Embed(title="エラー！", description=":x:入力された「x_url」がX（Twitter）のURLではありません！\n入力された内容を確認してください。:x:", color=0xff0000)
            else:
                embed=discord.Embed(title="Error!", description=":x:The [x_url] entered is not a X(Twitter) URL! \nPlease check the information you have entered.:x:", color=0xff0000)

            await interaction.followup.send(embed=embed)
            return
        
        # サーバーのデータが存在しているかを確認
        files = glob.glob('./data/guild_data/*.ndjson')
        judge = 0

        for i in range(0, len(files)):
            #print(os.path.split(files[i])[1])
            if(os.path.split(files[i])[1] == str(interaction.guild.id) + ".ndjson"):
                #print("一致しました！")
                judge = 1
                break
        
        if judge == 1:

            # 同じユーザーは登録できないようにする判定
            with open('./data/guild_data/' + str(interaction.guild.id) + ".ndjson") as f:
                read_data = ndjson.load(f)

            for i in range(0, len(read_data)):
                if int(read_data[i]["member"]) == member:
                    if language == "ja":
                        embed=discord.Embed(title="エラー！", description=":x:このユーザーの情報は既に登録されています。:x:", color=0xff0000)
                    else:
                        embed=discord.Embed(title="Error!", description=":x:This user's information has already been registered.:x:", color=0xff0000)

                    await interaction.followup.send(embed=embed)
                    return

            for i in range(0, len(read_data)):
                if read_data[i]["name"] == name:
                    if language == "ja":
                        embed=discord.Embed(title="エラー！", description=":x:この名前の情報は既に登録されています。:x:", color=0xff0000)
                    else:
                        embed=discord.Embed(title="Error!", description=":x:Information on this name has already been registered.:x:", color=0xff0000)

                    await interaction.followup.send(embed=embed)
                    return

            # 割り込ませる番号がデータがある数を超えていないか
            if number_interrupt != None:
                if len(read_data) < number_interrupt:
                    if language == "ja":
                        embed=discord.Embed(title="エラー！", description=":x:「number_interrupt」の値があるデータ数を超えています。:x:", color=0xff0000)
                    else:
                        embed=discord.Embed(title="Error!", description=":x:The value of [number_interrupt] exceeds a certain number of data.:x:", color=0xff0000)

                    await interaction.followup.send(embed=embed)
                    return

                if number_interrupt == 0:
                    if language == "ja":
                        embed=discord.Embed(title="エラー！", description=":x:「number_interrupt」の値に0は指定できません。:x:", color=0xff0000)
                    else:
                        embed=discord.Embed(title="Error!", description=":x:0 cannot be specified for the [number_interrupt] value.:x:", color=0xff0000)

                    await interaction.followup.send(embed=embed)
                    return
        else:
            # 割り込ませる番号がデータがないのに入力されていた場合のエラー
            if number_interrupt != None:
                if language == "ja":
                    embed=discord.Embed(title="エラー！", description=":x:このサーバーにはデータが存在しないため、「number_interrupt」の入力を受け付けることができません。:x:", color=0xff0000)
                else:
                    embed=discord.Embed(title="Error!", description=":x:This server cannot accept [number_interrupt] input because no data exists on this server.:x:", color=0xff0000)

                await interaction.followup.send(embed=embed)
                return

        # X(Twitter)のユーザー名を取り出す
        split_x_url = x_url.split('/')
        split_x_url = split_x_url[3].split('?')

        x_name = split_x_url[0]
        print(x_name)
            
        # 入力された内容をndjsonに書き込んでいく
        # guild_dataがあるかの確認
        content = {
            "name" : name,
            "member" : str(member),
            "stream_site_url" : stream_site_url,
            "x_name" : x_name
        }

        # number_intterupt 順番割込みの指定があった場合に使うread_data
        with open('./data/guild_data/' + str(interaction.guild.id) + ".ndjson") as f:
            read_data = ndjson.load(f)

        if number_interrupt == None:
            with open('./data/guild_data/' + str(interaction.guild.id) +".ndjson", 'a') as f:
                writer = ndjson.writer(f)
                writer.writerow(content)
        else:
            os.remove('./data/guild_data/' + str(interaction.guild.id) + ".ndjson")
            
            count = 0
            with open('./data/guild_data/' + str(interaction.guild.id) +".ndjson", 'a') as f:
                for i in range(0, len(read_data) + 1):
                    if i == number_interrupt - 1:
                        writer = ndjson.writer(f)
                        writer.writerow(content)
                    else:
                        writer = ndjson.writer(f)
                        writer.writerow(read_data[count])
                        count += 1
        
        if language == "ja":
            embed=discord.Embed(title="登録しました!", description="\n\n入力された情報を登録しました。\n\nユーザー：<@" + 
                                str(member) + ">\n登録名：" + name +"\n配信サイトURL：" + stream_site_url + 
                                "\n X（旧Twitter）URL：" + "https://x.com/" + x_name, color=0x00ff7f) 
        else:
            embed=discord.Embed(title="Registered!", description="\n\nThe entered information has been registered. \nUser: <@" + 
                                str(member) + ">\nRegistered name:" + name +"\nStream site URL:" + stream_site_url + 
                                "\n X (Twitter) URL:" + "https://x.com/" + x_name, color=0x00ff7f)             
        
        await interaction.followup.send(embed=embed)