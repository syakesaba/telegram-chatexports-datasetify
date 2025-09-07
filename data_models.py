from typing import (
    Optional,
    List,
    Union,
)
from pydantic import (
    BaseModel,
    Field,
)


class MessageEntity(BaseModel):
    """
    Telegramのテキストメッセージ内の特殊なエンティティを表すオブジェクトです。
    これには、ハッシュタグ、ユーザー名、URL、テキストの書式設定（太字、斜体など）などが含まれます。
    """

    type: str = Field(
        ...,
        description="""
        エンティティのタイプです。
        現在、以下のいずれかの値を取ります:
        'unknown', 'mention', 'hashtag', 'bot_command', 'link', 'email', 'bold', 'italic',
        'code', 'pre', 'plain', 'text_link', 'mention_name', 'phone', 'cashtag', 'underline',
        'strikethrough', 'blockquote', 'spoiler', 'custom_emoji'。
    """,
    )
    text: str = Field(
        ..., description="このエンティティが適用されるテキストの文字列です。"
    )


class Location(BaseModel):
    """
    共有された位置情報メッセージにおける、地図上の特定の地点を表すオブジェクトです。
    """

    latitude: float = Field(..., description="送信者によって定義された位置の緯度です。")
    longitude: float = Field(
        ..., description="送信者によって定義された位置の経度です。"
    )


class Invoice(BaseModel):
    """
    Telegram上での取引に関連する請求書の基本情報を含むオブジェクトです。
    """

    title: str = Field(..., description="請求書のタイトルです。")
    description: str = Field(..., description="請求書の説明です。")
    amount: int = Field(
        ...,
        description="""
        商品の価格を最小通貨単位で表したものです（整数型）。
        例えば、1.45米ドルの場合は145と表されます。
        通貨ごとの小数点以下の桁数については、currencies.jsonの`exp`パラメータを参照してください。
    """,
    )
    currency: str = Field(
        ..., description="3文字のISO 4217通貨コードです (例: USD, JPY)。"
    )
    receipt_message_id: Optional[int] = Field(
        None, description="関連するレシートメッセージのIDです (オプション)。"
    )


class PollAnswer(BaseModel):
    """
    Telegramの投票における特定の回答オプションを表すオブジェクトです。
    """

    text: str = Field(..., description="回答オプションのテキストです (1-100文字)。")
    voters: int = Field(..., description="この回答オプションに投票した人の数です。")
    chosen: str = Field(
        ...,
        description="""
        エクスポートを実行したユーザーがこの回答を選択した場合に'true'、
        そうでなければ'false'となる文字列です (真偽値ではなく文字列として定義されています)。
    """,
    )


class Poll(BaseModel):
    """
    Telegramの投票（アンケート）を表すオブジェクトです。
    """

    question: str = Field(..., description="投票の質問文です (1-300文字)。")
    closed: str = Field(
        ...,
        description="""
        投票が既に終了している場合に'true'、そうでなければ'false'となる文字列です
        (真偽値ではなく文字列として定義されています)。
    """,
    )
    total_voters: int = Field(..., description="投票の総投票者数です。")
    answers: List[PollAnswer] = Field(
        ...,
        description="投票の各回答オプションを表す`PollAnswer`オブジェクトの配列です。",
    )


class Giveaway(BaseModel):
    """
    Telegramのプレゼント企画（ギブアウェイ）に関する情報を含むオブジェクトです。
    """

    quantity: int = Field(
        ...,
        description="このプレゼント企画で配布されるサブスクリプションの総数です。",
    )
    months: int = Field(
        ...,
        description="このプレゼント企画で当選した場合に獲得できるサブスクリプションの期間（月数）です。",
    )
    until_date: str = Field(
        ...,
        description="プレゼント企画が終了する日付です (ISO 8601タイムスタンプ形式、例: 2023-11-13T14:37:50)。",
    )
    channels: List[int] = Field(
        ..., description="プレゼント企画に参加しているチャンネルのIDの配列です。"
    )


class Contact(BaseModel):
    """
    電話帳の連絡先を表すオブジェクトです。
    """

    first_name: str = Field(..., description="連絡先のファーストネームです。")
    last_name: str = Field(..., description="連絡先のラストネームです。")
    phone_number: str = Field(..., description="連絡先の電話番号です。")
    date: Optional[str] = Field(
        None,
        description="この連絡先が作成された日時です (ISO 8601タイムスタンプ形式、オプション)。",
    )
    date_unixtime: Optional[str] = Field(
        None,
        description="この連絡先が作成された日時です (Unixタイムスタンプ形式、オプション)。",
    )


class FrequentContact(BaseModel):
    """
    ユーザーが頻繁にメッセージを送る可能性が高い連絡先（ユーザーまたはボット）を表すオブジェクトです。
    Telegramはこのデータを使用して、検索セクションの上部にある「People」ボックスや、アタッチメントメニューのボット候補を生成します。
    """

    id: int = Field(
        ...,
        description="""
        この連絡先に保存されているユーザーまたはボットの一意の識別子です。
        この数値は32ビットより大きくなる可能性がありますが、最大52ビットなので、
        Pythonの標準的な`int`型（任意精度）や、64ビット整数、倍精度浮動小数点型で安全に保存できます。
    """,
    )
    category: str = Field(
        ...,
        description="この連絡先のカテゴリです。現在、'people'、'inline_bots'、'calls'のいずれかです。",
    )
    type: str = Field(
        ...,
        description="""
        この連絡先のタイプです。現在、'user'、'private_channel'、'private_group'、
        'private_supergroup'、'public_channel'、'public_supergroup'のいずれかです。
    """,
    )
    name: str = Field(..., description="連絡先の名前です。")
    rating: float = Field(
        ...,
        description="""
        ユーザーがこの連絡先にメッセージを送る可能性を表す評価値です。
        評価が最も高い連絡先が、最もメッセージを送られる可能性が高いと判断されます。
    """,
    )


class Session(BaseModel):
    """
    Telegramの特定のアクティブなセッションを表すオブジェクトです。
    「設定 > プライバシーとセキュリティ > アクティブなセッション」に表示される詳細情報を含みます。
    """

    last_active: str = Field(
        ...,
        description="このセッションが最後にアクティブだった日時です (ISO 8601タイムスタンプ形式、例: 2023-11-13T14:37:50)。",
    )
    last_active_unixtime: str = Field(
        ...,
        description="このセッションが最後にアクティブだった日時です (Unixタイムスタンプ形式、例: 1699882670)。",
    )
    last_ip: str = Field(
        ...,
        description="このセッションが最後に使用された際のIPアドレスです (例: 192.0.2.1)。",
    )
    last_country: str = Field(
        ..., description="このセッションがアクティブだった最後の国です。"
    )
    last_region: str = Field(
        ..., description="このセッションがアクティブだった最後の地域です。"
    )
    application_name: str = Field(
        ...,
        description="セッションに使用されたアプリケーションの名前です (例: “Telegram Android”)。",
    )
    application_version: str = Field(
        ..., description="アプリケーションのバージョンです (例: “10.2.8”)。"
    )
    device_model: str = Field(
        ...,
        description="デバイスのモデル名です (例: “Google Pixel 7 Pro”, “Chrome 116”など)。",
    )
    platform: str = Field(
        ...,
        description="プラットフォームの名前です (例: “Windows”, “Android”など)。",
    )
    system_version: str = Field(
        ...,
        description="オペレーティングシステムのバージョンです (例: “Windows 11”, “SDK 34”など)。",
    )
    created: str = Field(
        ...,
        description="このセッションが作成された日時です (ISO 8601タイムスタンプ形式、例: 2022-06-03T19:53:50)。",
    )
    created_unixtime: str = Field(
        ...,
        description="このセッションが作成された日時です (Unixタイムスタンプ形式、例: 1654278830)。",
    )


class WebSession(BaseModel):
    """
    Telegramを介した認証を使用してログインしたWebサイトのセッションを表すオブジェクトです。
    この情報は「設定 > プライバシーとセキュリティ > アクティブなセッション」にも表示されます。
    """

    last_active: str = Field(
        ...,
        description="このWebセッションが最後にアクティブだった日時です (ISO 8601タイムスタンプ形式、例: 2023-11-13T14:37:50)。",
    )
    last_active_unixtime: str = Field(
        ...,
        description="このWebセッションが最後にアクティブだった日時です (Unixタイムスタンプ形式、例: 1699882670)。",
    )
    last_ip: str = Field(
        ...,
        description="このWebセッションが最後に使用された際のIPアドレスです (例: 192.0.2.1)。",
    )
    last_region: str = Field(
        ..., description="このWebセッションが最後にアクティブだった地域です。"
    )
    bot_username: str = Field(
        ...,
        description="このセッションの認証に使用されたボットのユーザー名です (例: TutorialBot)。",
    )
    domain_name: str = Field(
        ..., description="認証されたドメイン名です (例: core.telegram.org)。"
    )
    browser: str = Field(
        ..., description="ログインに使用されたブラウザです (例: “Chrome 113”)。"
    )
    platform: str = Field(
        ...,
        description="ログインに使用されたプラットフォームです (例: “Windows”)。",
    )
    created: str = Field(
        ...,
        description="このWebセッションが作成された日時です (ISO 8601タイムスタンプ形式、例: 2022-06-03T19:53:50)。",
    )
    created_unixtime: str = Field(
        ...,
        description="このWebセッションが作成された日時です (Unixタイムスタンプ形式、例: 1654278830)。",
    )


class StickerPack(BaseModel):
    """
    Telegramのステッカーパックを表すオブジェクトです。
    現在のバージョンのスキーマでは、ステッカーパックのURLのみを保持します。
    """

    url: str = Field(..., description="このステッカーパックのURLです。")


class CloudDraft(BaseModel):
    """
    「クラウドドラフト」とは、ユーザーがTelegramチャットの入力フィールドに残したが、
    まだ送信していないメッセージを指します。
    """

    chat: str = Field(
        ...,
        description="""
        ドラフトが作成されたチャットの識別子です。
        '<type> #<chat_id>'の形式で、例としては'user #12345678'や'bot #93372553'があります。
    """,
    )
    chat_name: str = Field(
        ...,
        description="ドラフトが作成されたチャットの名前です (例: “BotFather”)。",
    )
    html: str = Field(
        ...,
        description="""
        ドラフトのテキストコンテンツが有効なHTMLとしてレンダリングされたものです。
        テキスト内の書式設定は自動的にHTMLタグに変換されます。
    """,
    )


class Ip(BaseModel):
    """
    ユーザーがTelegramにアクセスしたIPアドレスを表すオブジェクトです。
    """

    ip: str = Field(..., description="IPアドレスの文字列です。")


class ChangeEvent(BaseModel):
    """
    ユーザーに関連する変更イベント（例: ユーザー名、名前、パスワード、電話番号の変更など）を表すオブジェクトです。
    """

    app_id: int = Field(..., description="イベントが発生したアプリケーションのIDです。")
    country: str = Field(
        ..., description="イベントが発生した国のISO 3166-1 alpha-2コードです。"
    )
    event: str = Field(
        ...,
        description="""
        イベントのタイプです。現在、以下のいずれかの値を取ります:
        'username_change', 'name_change', 'password_change', 'phone_change'。
    """,
    )
    ip: str = Field(..., description="イベント発生時のIPアドレスです。")
    phone_country: str = Field(
        ...,
        description="電話番号に基づいた、イベント発生時の国のISO 3166-1 alpha-2コードです。",
    )
    session_age: str = Field(
        ...,
        description="イベントが発生したセッションの経過時間（秒単位）です。文字列型として定義されています。",
    )
    timestamp: int = Field(..., description="イベントのUnixタイムスタンプです。")
    new_username: Optional[str] = Field(
        None,
        description="変更後のユーザー名です (username_changeイベントの場合に利用可能、オプション)。",
    )
    old_username: Optional[str] = Field(
        None,
        description="変更前のユーザー名です (username_changeイベントの場合に利用可能、オプション)。",
    )
    new_name: Optional[str] = Field(
        None,
        description="変更後の名前です (name_changeイベントの場合に利用可能、オプション)。",
    )
    old_name: Optional[str] = Field(
        None,
        description="変更前の名前です (name_changeイベントの場合に利用可能、オプション)。",
    )
    new_phone: Optional[str] = Field(
        None,
        description="変更後の電話番号です (phone_changeイベントの場合に利用可能、オプション)。",
    )
    old_phone: Optional[str] = Field(
        None,
        description="変更前の電話番号です (phone_changeイベントの場合に利用可能、オプション)。",
    )
    email: Optional[str] = Field(
        None,
        description="変更前のメールアドレスです (password_changeイベントの場合に利用可能、オプション)。",
    )
    new_email: Optional[str] = Field(
        None,
        description="変更後のメールアドレスです (password_changeイベントの場合に利用可能、オプション)。",
    )
    hint: Optional[str] = Field(
        None,
        description="パスワードヒントです (password_changeイベントの場合に利用可能、オプション)。",
    )


class UserProfilePhoto(BaseModel):
    """
    ユーザーのプロフィール写真の記録を表すオブジェクトです。
    """

    date: str = Field(
        ...,
        description="この写真がアップロードされた日時です (ISO 8601タイムスタンプ形式、例: 2021-12-28T18:53:27)。",
    )
    date_unixtime: str = Field(
        ...,
        description="この写真がアップロードされた日時です (Unixタイムスタンプ形式、例: 1640714007)。",
    )
    photo: str = Field(
        ...,
        description="この写真ファイルへの相対パスです (例: profile_pictures/photo_1@28-12-2021_18-53-27.jpg)。",
    )


class Story(BaseModel):
    """
    ユーザーがTelegramモバイルアプリから投稿したストーリーを表すオブジェクトです。
    """

    date: str = Field(
        ...,
        description="このストーリーがアップロードされた日時です (ISO 8601タイムスタンプ形式、例: 2023-09-02T17:05:43)。",
    )
    date_unixtime: str = Field(
        ...,
        description="このストーリーがアップロードされた日時です (Unixタイムスタンプ形式、例: 1693667143)。",
    )
    expires: str = Field(
        ...,
        description="このストーリーの有効期限です (ISO 8601タイムスタンプ形式、例: 2023-09-03T17:05:43)。",
    )
    expires_unixtime: str = Field(
        ...,
        description="このストーリーの有効期限です (Unixタイムスタンプ形式、例: 1693753543)。",
    )
    pinned: bool = Field(
        ...,
        description="ストーリーがピン留めされている場合はTrue、そうでない場合はFalseです。",
    )
    media: str = Field(
        ...,
        description="ストーリーとしてアップロードされたメディアファイルへの相対パスです (例: stories/story_2@02-09-2023_17-05-43.mp4)。",
    )


# --- これらのオブジェクトをリストとして含むオブジェクト、または他のオブジェクトの一部となるオブジェクト ---


class PersonalInformation(BaseModel):
    """
    エクスポートされたユーザーに関する基本的な個人情報を含むオブジェクトです。
    """

    user_id: int = Field(
        ...,
        description="""
        このユーザーの一意の識別子です。
        この数値は32ビットより大きくなる可能性がありますが、最大52ビットなので、
        Pythonの標準的な`int`型（任意精度）や、64ビット整数、倍精度浮動小数点型で安全に保存できます。
    """,
    )
    phone_number: str = Field(
        ..., description="ユーザーの電話番号です (例: +01 234 567 8910)。"
    )
    first_name: str = Field(..., description="ユーザーのファーストネームです。")
    last_name: str = Field(..., description="ユーザーのラストネームです。")
    username: Optional[str] = Field(
        None,
        description="ユーザーの公開ユーザー名です (例: @username、オプション)。",
    )
    bio: Optional[str] = Field(
        None, description="ユーザーの自己紹介文です (オプション)。"
    )


class Contacts(BaseModel):
    """
    このエクスポートに含まれるすべての連絡先を含むオブジェクトです。
    ユーザーがアクセスを許可した場合、連絡先はTelegramと継続的に同期されます。
    """

    about: str = Field(
        ..., description="エクスポートされた連絡先データに関する簡単な説明です。"
    )
    list: List[Contact] = Field(
        ...,
        description="エクスポートされたすべての`Contact`オブジェクトの配列です。",
    )


class FrequentContacts(BaseModel):
    """
    ユーザーが頻繁にメッセージを送る可能性が高い連絡先を含むオブジェクトです。
    Telegramは、このデータを使用して検索セクションの上部にある「People」ボックスを生成したり、
    インラインボットを提案したりします。
    """

    about: str = Field(
        ...,
        description="エクスポートされた頻繁な連絡先データに関する簡単な説明です。",
    )
    list: List[FrequentContact] = Field(
        ...,
        description="エクスポートされたすべての`FrequentContact`オブジェクトのリストです。",
    )


class Sessions(BaseModel):
    """
    ユーザーのすべてのアクティブなTelegramセッションに関する情報を含むオブジェクトです。
    これは「設定 > プライバシーとセキュリティ > アクティブなセッション」に表示される情報と一致します。
    """

    about: str = Field(
        ...,
        description="エクスポートされたセッションデータに関する簡単な説明です。",
    )
    list: List[Session] = Field(
        ..., description="アクティブな`Session`オブジェクトの配列です。"
    )


class WebSessions(BaseModel):
    """
    Telegramを介した認証を使用してログインしたすべてのWebサイトに関する情報を含むオブジェクトです。
    この情報も「設定 > プライバシーとセキュリティ > アクティブなセッション」に表示されます。
    """

    about: str = Field(
        ...,
        description="エクスポートされたWebセッションデータに関する簡単な説明です。",
    )
    list: List[WebSession] = Field(
        ..., description="`WebSession`オブジェクトの配列です。"
    )


class OtherData(BaseModel):
    """
    ユーザーのIPアドレス履歴、ユーザー名や電話番号の変更履歴、作成・インストールしたステッカーパック、
    クラウドドラフトなど、その他の様々なデータを含むオブジェクトです。
    """

    about_meta: str = Field(
        ..., description="エクスポートされたその他のデータに関する簡単な説明です。"
    )
    help: str = Field(
        ...,
        description="**OtherData**フィールドが現在ベータ版であることに関する一時的な免責事項です。",
    )
    changes_log: List[ChangeEvent] = Field(
        ...,
        description="このユーザーに関連するイベント（ユーザー名変更、電話番号変更など）の配列です。",
    )
    created_stickers: List[StickerPack] = Field(
        ..., description="ユーザーが作成したステッカーパックの配列です。"
    )
    drafts: List[CloudDraft] = Field(
        ...,
        description="ユーザーが送信せずに残したクラウドドラフトメッセージの配列です。",
    )
    drafts_about: str = Field(
        ..., description="クラウドドラフトに関する簡単な説明です。"
    )
    installed_stickers: List[StickerPack] = Field(
        ..., description="ユーザーがインストールしたステッカーパックの配列です。"
    )
    ips: List[Ip] = Field(
        ...,
        description="過去12ヶ月間にこのユーザーがTelegramにアクセスしたIPアドレスの配列です。",
    )
    email_about: str = Field(..., description="現在、このフィールドは空です。")


# --- チャットとメッセージ関連のオブジェクト (これらは他のオブジェクトを参照するため、上位に配置) ---


class Message(BaseModel):
    """
    個々のメッセージを表すオブジェクトです。
    このオブジェクトは非常に多くのフィールドを持つため、注意深く確認してください。
    なお、メディアパスは、エクスポートのメディアサイズ閾値やメディアタイプ除外フィルターによって、
    実際のパスではなく警告メッセージに置き換えられる場合があります。
    """

    id: int = Field(..., description="このチャット内での一意のメッセージ識別子です。")
    type: str = Field(
        ...,
        description="メッセージのタイプです。通常のメッセージの場合は'message'、サービスメッセージの場合は'service'です。",
    )
    action: Optional[str] = Field(
        None,
        description="""
        サービスメッセージの場合のアクションタイプです (オプション)。
        例: 'create_group', 'edit_group_title', 'pin_message'など、多岐にわたります。
    """,
    )
    date: str = Field(
        ...,
        description="メッセージが送信された日時です (ISO 8601タイムスタンプ形式、例: 2023-09-03T17:05:43)。",
    )
    date_unixtime: str = Field(
        ...,
        description="メッセージが送信された日時です (Unixタイムスタンプ形式、例: 1693753543)。",
    )
    from_sender: Optional[str] = Field(
        None,
        alias="from",
        description="""
        メッセージ送信者の名前です (オプション)。
        'proximity_reached'アクションでは、'to'フィールドで指定されたユーザーまたはチャットに近接したユーザーまたはチャットの名前を表します。
        (`from`はPythonの予約語であるため、フィールド名を`from_sender`とし、JSONとの対応のために`alias="from"`を設定しています。)
    """,
    )
    from_id: Optional[str] = Field(
        None,
        description="""
        送信者のIDです (例: user123456, channel123456, chat123456のように'<type><id>'形式)。
        'proximity_reached'アクションでは、'to_id'に近接したユーザーまたはチャットを表します (オプション)。
    """,
    )
    edited: Optional[str] = Field(
        None,
        description="メッセージが編集された日時です (ISO 8601タイムスタンプ形式、例: 2023-09-03T17:05:43、オプション)。",
    )
    edited_unixtime: Optional[str] = Field(
        None,
        description="メッセージが編集された日時です (Unixタイムスタンプ形式、例: 1693753543、オプション)。",
    )
    reply_to_message_id: Optional[int] = Field(
        None,
        description="このメッセージが他のメッセージへの返信である場合、元のメッセージのIDです (オプション)。",
    )
    text: Union[str, List[Union[str, MessageEntity]]] = Field(
        ...,
        description="""
        メッセージのテキストコンテンツです。
        エンティティ（書式設定、リンクなど）がない場合は単一の文字列です。
        エンティティがある場合は、`MessageEntity`オブジェクトと生の文字列が混在する配列として表現されます。
        特に'plain'タイプのエンティティは、配列内で単一の文字列として展開されて表現されます。
    """,
    )
    text_entities: List[MessageEntity] = Field(
        ...,
        description="""
        メッセージのテキストを`MessageEntity`オブジェクトの配列として表現したものです。
        メッセージのすべての部分がエンティティとして扱われ、プレーンテキストも'plain'タイプのエンティティとして表されます。
    """,
    )
    members: Optional[List[str]] = Field(
        None,
        description="""
        `create_group`, `invite_members`, `remove_members`, `invite_to_group_call`などの
        特定のアクションメッセージで利用可能なメンバーのリストです (オプション)。
    """,
    )
    actor: Optional[str] = Field(
        None,
        description="""
        アクションを実行したユーザーまたはエンティティの名前です (アクションが定義されている場合、オプション)。
    """,
    )
    actor_id: Optional[str] = Field(
        None,
        description="""
        アクションを実行したユーザーまたはエンティティのIDです (例: user123456)。
        アクションが定義されている場合に利用可能です (オプション)。
    """,
    )
    photo: Optional[str] = Field(
        None,
        description="""
        メッセージが写真の場合の、写真ファイルへの相対パスです。
        `edit_group_photo`や`suggest_profile_photo`などの互換性のあるアクションでも利用可能です (オプション)。
    """,
    )
    width: Optional[float] = Field(
        None,
        description="""
        メディアの幅です (互換性のあるメディアで利用可能、オプション)。
    """,
    )
    height: Optional[float] = Field(
        None,
        description="""
        メディアの高さです (互換性のあるメディアで利用可能、オプション)。
    """,
    )
    file: Optional[str] = Field(
        None,
        description="メッセージに互換性のあるファイルメディアがある場合の、ファイルへの相対パスです (オプション)。",
    )
    thumbnail: Optional[str] = Field(
        None,
        description="メディアのサムネイルファイルへの相対パスです (存在する場合、オプション)。",
    )
    self_destruct_period_seconds: Optional[int] = Field(
        None,
        description="""
        このメッセージの有効期間（秒単位）です (自己破壊メッセージで利用可能、オプション)。
    """,
    )
    title: Optional[str] = Field(
        None,
        description="""
        チャット、トピック、または音楽のタイトルです (例: `create_group`, `create_channel`などのアクションや
        `audio_file`メディアタイプで利用可能、オプション)。
    """,
    )
    inviter: Optional[str] = Field(
        None,
        description="""
        招待リンクを作成したユーザーの名前です (`join_group_by_link`アクションで利用可能、オプション)。
    """,
    )
    message_id: Optional[int] = Field(
        None,
        description="""
        アクションが参照するメッセージのIDです (`pin_message`や`set_same_chat_wallpaper`で利用可能、オプション)。
    """,
    )
    game_message_id: Optional[int] = Field(
        None,
        description="ゲームスコアメッセージのIDです (`score_in_game`アクションで利用可能、オプション)。",
    )
    score: Optional[int] = Field(
        None,
        description="ゲームスコアです (`score_in_game`アクションで利用可能、オプション)。",
    )
    amount: Optional[int] = Field(
        None,
        description="""
        製品の価格を最小通貨単位で表したものです (整数型)。
        `send_payment`アクションで利用可能、オプション。
    """,
    )
    currency: Optional[str] = Field(
        None,
        description="""
        3文字のISO 4217通貨コードです (`send_payment`アクションで利用可能、オプション)。
    """,
    )
    invoice_message_id: Optional[int] = Field(
        None,
        description="請求書メッセージのIDです (`send_payment`アクションで利用可能、オプション)。",
    )
    recurring: Optional[str] = Field(
        None,
        description="""
        `send_payment`アクションでの支払いタイプです。
        利用可能な場合、'used'または'init'のいずれかです (オプション)。
    """,
    )
    duration_seconds: Optional[int] = Field(
        None,
        description="期間（秒単位）です (`phone_call`アクションや互換性のあるメディアで利用可能、オプション)。",
    )
    discard_reason: Optional[str] = Field(
        None,
        description="""
        通話が破棄された理由です (`phone_call`アクションで利用可能、オプション)。
        利用可能な場合、'busy', 'disconnect', 'hangup', 'missed'のいずれかです。
    """,
    )
    information_text: Optional[str] = Field(
        None, description="カスタムアクションテキストです (オプション)。"
    )
    reason_app_id: Optional[int] = Field(
        None,
        description="""
        ボットがメッセージを送信することを許可したアプリのIDです (`allow_sending_messages`アクションで利用可能、オプション)。
    """,
    )
    reason_app_name: Optional[str] = Field(
        None,
        description="""
        ボットがメッセージを送信することを許可したアプリの名前です (`allow_sending_messages`アクションで利用可能、オプション)。
    """,
    )
    reason_domain: Optional[str] = Field(
        None,
        description="""
        Telegramログイン機能を使用してボットがメッセージを送信することを許可したドメインです
        (`allow_sending_messages`アクションで利用可能、オプション)。
    """,
    )
    values: Optional[List[str]] = Field(
        None,
        description="""
        要求されたセキュアなTelegram Passportの値のタイプです
        (`send_passport_values`アクションで利用可能、オプション)。
    """,
    )
    to_id: Optional[int] = Field(
        None,
        description="""
        ライブ位置情報近接アラートを購読しているユーザーまたはチャットのIDです (`proximity_reached`アクションで利用可能、オプション)。
    """,
    )
    to: Optional[str] = Field(
        None,
        description="""
        ライブ位置情報近接アラートを購読しているユーザーまたはチャットの名前です (`proximity_reached`アクションで利用可能、オプション)。
    """,
    )
    distance: Optional[int] = Field(
        None,
        description="""
        距離（メートル単位、0-100000）です (`proximity_reached`アクションで利用可能、オプション)。
    """,
    )
    period: Optional[int] = Field(
        None,
        description="""
        このチャットで送信されたすべてのメッセージの新しいTime-To-Liveです。
        0の場合、自動削除は無効です (`set_messages_ttl`アクションで利用可能、オプション)。
    """,
    )
    schedule_date: Optional[int] = Field(
        None,
        description="""
        このグループ通話が開始される予定日時です (`group_call_scheduled`アクションで利用可能、オプション)。
    """,
    )
    emoticon: Optional[str] = Field(
        None,
        description="""
        チャットテーマを識別する絵文字です (`edit_chat_theme`アクションで利用可能、オプション)。
    """,
    )
    cost: Optional[str] = Field(
        None,
        description="""
        贈られたTelegram Premiumサブスクリプションの価格を最小通貨単位で表したものです (文字列型)。
        `send_premium_gift`アクションで利用可能、オプション。
    """,
    )
    months: Optional[int] = Field(
        None,
        description="""
        贈られたTelegram Premiumサブスクリプションの期間（月数）です
        (`send_premium_gift`および`gift_code_prize`アクションで利用可能、オプション)。
    """,
    )
    new_title: Optional[str] = Field(
        None,
        description="""
        新しいトピックのタイトルです (`topic_edit`アクションで利用可能、オプション)。
    """,
    )
    new_icon_emoji_id: Optional[str] = Field(
        None,
        description="""
        新しいトピックのアイコン絵文字IDです (`topic_edit`アクションで利用可能、オプション)。
    """,
    )
    button_id: Optional[int] = Field(
        None,
        description="""
        `keyboardButtonRequestPeer`ボタンに含まれるボタンIDです (`requested_peer`アクションで利用可能、オプション) [16, 17]。
    """,
    )
    peer_id: Optional[int] = Field(
        None,
        description="共有されたピアIDです (`requested_peer`アクションで利用可能、オプション)。",
    )
    author: Optional[str] = Field(
        None,
        description="""
        署名が有効なチャンネル投稿の場合、このメッセージの作成者の名前です (オプション)。
    """,
    )
    forwarded_from: Optional[str] = Field(
        None,
        description="このメッセージが転送された元のピアの名前です (オプション)。",
    )
    saved_from: Optional[str] = Field(
        None,
        description="このメッセージが保存されたチャットの名前です (オプション)。",
    )
    via_bot: Optional[str] = Field(
        None,
        description="メッセージがボットを介して送信された場合、そのボットのユーザー名です (オプション)。",
    )
    media_type: Optional[str] = Field(
        None,
        description="""
        このメッセージのメディアタイプです (存在する場合、オプション)。
        'sticker', 'video_message', 'voice_message', 'animation', 'video_file', 'audio_file'のいずれかです。
    """,
    )
    performer: Optional[str] = Field(
        None,
        description="このメディアのパフォーマーです (`audio_file`メディアタイプで利用可能、オプション)。",
    )
    mime_type: Optional[str] = Field(
        None,
        description="メディアのMIMEタイプです (ステッカーでは利用不可、オプション)。",
    )
    contact_information: Optional[Contact] = Field(
        None,
        description="共有された連絡先情報です (`Contact`オブジェクト、オプション)。",
    )
    contact_vcard: Optional[str] = Field(
        None,
        description="連絡先のエクスポートされたvcardファイルへの相対パスです (オプション)。",
    )
    location_information: Optional[Location] = Field(
        None,
        description="""
        メッセージが共有された位置情報である場合の、位置情報です (`Location`オブジェクト、オプション)。
    """,
    )
    live_location_period_seconds: Optional[int] = Field(
        None,
        description="""
        ライブ位置情報の場合、位置情報を共有する期間（秒単位）です (オプション)。
    """,
    )
    place_name: Optional[str] = Field(
        None, description="ユーザーが共有した場所の名前です (オプション)。"
    )
    address: Optional[str] = Field(
        None, description="ユーザーが共有した場所の物理アドレスです (オプション)。"
    )
    game_title: Optional[str] = Field(
        None,
        description="このメッセージを介して送信されたHTML5ゲームのタイトルです (オプション)。",
    )
    game_description: Optional[str] = Field(
        None,
        description="このメッセージを介して送信されたHTML5ゲームの説明です (オプション)。",
    )
    game_link: Optional[str] = Field(
        None,
        description="このメッセージを介して送信されたHTML5ゲームへのリンクです (オプション)。",
    )
    invoice_information: Optional[Invoice] = Field(
        None,
        description="Telegram上の取引に対する請求書です (`Invoice`オブジェクト、オプション)。",
    )
    poll: Optional[Poll] = Field(
        None, description="Telegramの投票です (`Poll`オブジェクト、オプション)。"
    )
    gift_code: Optional[str] = Field(
        None,
        description="ギフトコードです (`gift_code_prize`アクションで利用可能、オプション)。",
    )
    boost_peer_id: Optional[int] = Field(
        None,
        description="""
        ギフトコードを作成したチャットまたはユーザーの識別子です (`gift_code_prize`アクションで利用可能、オプション)。
    """,
    )
    unclaimed: Optional[bool] = Field(
        None,
        description="ギフトコードが未請求の場合にTrueです (`gift_code_prize`アクションで利用可能、オプション)。",
    )
    via_giveaway: Optional[bool] = Field(
        None,
        description="ギフトコードがプレゼント企画のために作成された場合にTrueです (`gift_code_prize`アクションで利用可能、オプション)。",
    )
    giveaway_information: Optional[Giveaway] = Field(
        None,
        description="Telegramのプレゼント企画情報です (`Giveaway`オブジェクト、オプション)。",
    )


class Chat(BaseModel):
    """
    個々のチャット（会話）を表すオブジェクトです。
    公開グループやチャンネルのエクスポートでは、エクスポートをリクエストしたユーザーが送信したメッセージのみが含まれることに注意してください。
    """

    id: int = Field(
        ...,
        description="""
        このチャットの一意の識別子です。
        この数値は32ビットより大きくなる可能性がありますが、最大52ビットなので、
        Pythonの標準的な`int`型（任意精度）や、署名付き64ビット整数、倍精度浮動小数点型で安全に保存できます。
    """,
    )
    name: str = Field(..., description="チャットの名前です。")
    type: str = Field(
        ...,
        description="""
        チャットのタイプです。現在、以下のいずれかの値を取ります:
        'saved_messages', 'replies', 'personal_chat', 'bot_chat', 'private_group',
        'private_supergroup', 'public_supergroup', 'private_channel', 'public_channel'。
    """,
    )
    messages: List[Message] = Field(
        ..., description="このチャット内の`Message`オブジェクトの配列です。"
    )


class Chats(BaseModel):
    """
    エクスポートに含まれるすべてのチャットのリストを含むオブジェクトです。
    """

    about: str = Field(
        ..., description="エクスポートされたチャットデータに関する簡単な説明です。"
    )
    list: List[Chat] = Field(
        ..., description="エクスポートされたすべての`Chat`オブジェクトの配列です。"
    )


class LeftChats(BaseModel):
    """
    ユーザーが退出した、またはBANされたスーパーグループとチャンネルのリストを含むオブジェクトです。
    """

    about: str = Field(
        ..., description="ユーザーが退出したチャットデータに関する簡単な説明です。"
    )
    list: List[Chat] = Field(
        ...,
        description="ユーザーが退出した、またはBANされた`Chat`オブジェクトの配列です。",
    )
