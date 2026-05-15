# VTuberDescriptionCreateBot

## 招待URL / Invite URL

* [Invite](https://discord.com/api/oauth2/authorize?client_id=1165165952611127306&permissions=92160&scope=bot%20applications.commands)

## 一緒に開発した方 / Those who developed the Bot together

* 星尾ながる☄️⛈️ / Hoshio Nagaru☄️⛈️
  * このBot作成の企画をし、機能全てを考えた方です！ / He is the person who planned the creation of this bot and thought of all the features!
  * X(Twitter):[https://twitter.com/Nagaru_ST7](https://twitter.com/Nagaru_ST7)

## 概要 / Expanation

* このBotはVTuberがコラボの時などに作る概要欄作成を支援するBotです。

* This bot work on the discord. This bot helps VTubers create description that they create for collaborations.

## Discord上でBotを作る際に必要なインテント・権限 / Intents and permissions required to create a Bot on Discord

* インテント / Intents
  * SERVER MEMBERS INTENT

* 権限 / Permissions
  * Scopes
    * bot
    * applications.commands

  * permissions
    * Send Messages
    * Manage Messages
    * Embed Links
    * Read MEssage History


## 使い方（プログラムの動作のさせ方） / How to Use (How to run the program)

**Japanese**

※DiscordのBotの作成やトークンの取得はできている前提で説明させていただきます。

※Botをプログラム側で起動できたことが確認できるまで、サーバーへBotの招待を行わないでください。
* これは、サーバーの入退出でそれを判定するファイルが生成される仕様にしたためです。そのため、先にBotが起動していない状態でサーバーへ招待を行うとコマンドの使用ができません。申し訳ないです。

1. 最初にPythonをインストールしてください。（導入済みの方は飛ばしていただいて結構です。）

※もしかしたら導入済みの可能性もありますので、Windowsの場合はコマンドプロンプト、Linuxの場合はターミナルで「python --version」と打ち、「Python 〇.〇.〇」みたいな表記がでれば導入されているかが確認できます。

* Windows：[Link](https://www.javadrive.jp/python/install/index1.html)
* Linux(Ubuntu)：[Link](https://self-development.info/ubuntu%E3%81%AB%E6%9C%80%E6%96%B0%E3%83%90%E3%83%BC%E3%82%B8%E3%83%A7%E3%83%B3%E3%81%AEpython%E3%82%92%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB%E3%81%99%E3%82%8B/)

2. 次にこのページの１番上の方にある、「Code」を押して、「Download ZIP」を押しファイルをダウンロードします。（Linuxでターミナルで行っている場合はgit clone等を使用して、ダウンロードしてください。）

3. そしてそのファイルを解凍し、「.env」をテキストエディタで開き、「your_discord_bot_token」という部分にDiscordのBotトークンを入れてください。

※「.env」が見えない場合、隠しファイル扱いとなっている可能性が高いため、下記を参考に表示できるようにしてください。

* Windows10：[Link](https://pc-karuma.net/windows-10-show-hidden-files-folders/)
* Windows11：[Link](https://www.fmworld.net/cs/azbyclub/qanavi/jsp/qacontents.jsp?PID=8511-2971)
* Linux(Ubuntu かつ デスクトップ画面からの操作の場合)：[Link](https://linuxfan.info/show-hidden-files-in-nautilus#toc_id_3)

4. コマンドプロンプトまたは、ターミナルで「main.py」があるディレクトリまで移動し、「pip install -r requirements.txt」を打ってから、「python main.py」と打つことでプログラムを開始し、使用することが可能になります。

※ディレクトリの移動方法
* Windowsの場合は簡単な操作でそのディレクトリからコマンドプロンプトを起動する方法があります。 → [Link](https://qiita.com/windows222/items/2ac133a244f4a9527022)
* Linux(Ubuntu)の場合：[Link](https://uxmilk.jp/27431)


**English**

※The explanation assumes that the Discord Bot has been created and the token has been obtained.

※Please do not invite the Bot to the server until you can confirm that the Bot has been started on the program side.
* This is because a file to determine this is generated upon server entry and exit. Therefore, if you invite the bot to the server before it is started, you will not be able to use the commands. We apologize for the inconvenience.

1. First, please install Python. (If you have already installed it, you can skip this step.)

※There is a possibility that it is already installed, so you can check if it is installed by typing `python --version` in the command prompt for Windows, or the terminal for Linux. If a notation like `Python 〇.〇.〇` appears, it is installed.

* Windows: [Link](https://www.javadrive.jp/python/install/index1.html)
* Linux(Ubuntu): [Link](https://self-development.info/ubuntu%E3%81%AB%E6%9C%80%E6%96%B0%E3%83%90%E3%83%BC%E3%82%B8%E3%83%A7%E3%83%B3%E3%81%AEpython%E3%82%92%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB%E3%81%99%E3%82%8B/)

2. Next, click on "Code" at the top of this page, and then click "Download ZIP" to download the file. (If you are using a terminal in Linux, please use git clone, etc. to download.)

3. Then, unzip the file, open `.env` with a text editor, and put your Discord Bot token in the part that says `your_discord_bot_token`.

※If you cannot see `.env`, there is a high possibility that it is treated as a hidden file, so please refer to the following so that it can be displayed.

* Windows10: [Link](https://pc-karuma.net/windows-10-show-hidden-files-folders/)
* Windows11: [Link](https://www.fmworld.net/cs/azbyclub/qanavi/jsp/qacontents.jsp?PID=8511-2971)
* Linux(Ubuntu and desktop operation): [Link](https://linuxfan.info/show-hidden-files-in-nautilus#toc_id_3)

4. Navigate to the directory where `main.py` is located in the command prompt or terminal, type `pip install -r requirements.txt`, and then type `python main.py` to start and use the program.

※How to move directories
* In the case of Windows, there is a way to start the command prompt from that directory with a simple operation. → [Link](https://qiita.com/windows222/items/2ac133a244f4a9527022)
* In the case of Linux(Ubuntu): [Link](https://uxmilk.jp/27431)


## Discord上での使い方 / How to ues? (on the Discord)

下記のスラッシュコマンドを入力して使うことができます。 / It can be used by entering the following slash command

**Japanese**

* /inforaction add
  * name:[表示させたい名前]
  * member:[どのDiscordユーザーに結びつけるか]
  * stream_site_url[配信しているサイトのURL]
  * x_url:[X（Twitter）のURL]
  * number_interrupt:[登録されている番号のどこに割り込ませたいか]

* /information delete

* /information list

* /order change

* /description
  * role:[概要欄生成をさせたいユーザーのロール]
  * display_x:[X（Twitter）の欄を表示させるかどうか（ON/OFF）]
  * title:[敬称の指定]
 
* /hashtag role:[ハッシュタグ生成をさせたいユーザーのロール]

* /template
  * role:[概要欄生成をさせたいユーザーのロール]
  * display_x:[X（Twitter）の欄を表示させるかどうか（ON/OFF）]
  * title:[敬称の指定]
 
* /language language:[言語の選択（ja/en）]

* /help

**English**

* /inforaction add
  * name:[name you want to display]
  * member:[which Discord user to link to]
  * stream_site_url[URL of the site you are distributing]
  * x_url:[X (Twitter)]
  * number_interrupt:[where in the registered number you want to interrupt]

* /information delete

* /information list

* /order change

* /description
  * role:[Role of the user for whom you want the summary field generation]
  * display_x:[Whether to display the X (Twitter) field (ON/OFF)]
  * title:[Respected title designation]
 
* /hashtag role:[the role of the user you want to have hashtag generation]

* /template
  * role:[role of user you want to have summary field generation]
  * display_x:[whether to display X (Twitter) field (ON/OFF)]
  * title:[specify honorific title]
 
* /language language:[Select language (ja/en)]

* /help