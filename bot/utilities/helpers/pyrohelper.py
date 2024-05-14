from pyrogram import raw
from pyrogram.client import Client

from bot.config import config


class NoInviteLinkError(Exception):
    def __init__(self, channel: int | str) -> None:
        super().__init__(f"{channel} has no invite link")


class PyroHelper:
    """Helper class for additional Pyrogram functions."""

    @staticmethod
    async def get_channel_invites(client: Client, channels: list[int]) -> dict[str, int]:
        """
        Get invite links for a list of channels.

        Parameters:
            client (Client):
                Pyrogram client instance.
            channels (list[int]):
                List of channel IDs to get invite links for.

        Returns:
            dict[str, int]:
                Dictionary with channel titles as keys and their invite links as values.

        Raises:
            ValueError:
                If any channel in the list does not have an invite link.

        Example:
            make sure the bot have required permissions to get invites
            >>> helper = PyroHelper()

            >>> channels = [123456789, 987654321]
            >>> invite_links = await helper.get_channel_invites(app, channels)
            >>> print(invite_links)
            {
                "Channel Title 1": "https://t.me/joinchat/ABCDE...",
                "Channel Title 2": "https://t.me/joinchat/FGHIJ..."
            }
        """
        channels_n_invite = {}
        for channel_id in channels:
            channel = await client.get_chat(chat_id=channel_id)
            get_link = await client.invoke(
                raw.functions.messages.ExportChatInvite(  # type: ignore[reportPrivateImportUsage]
                    peer=await client.resolve_peer(peer_id=channel_id),  # type: ignore[reportArgumentType]
                    legacy_revoke_permanent=True,
                    request_needed=config.PRIVATE_REQUEST,
                ),
            )

            if get_link is not None:
                channel_invite = get_link.link  # type: ignore[reportAttributeAccessIssue]
                channels_n_invite[channel.title] = channel_invite
            else:
                raise NoInviteLinkError(channel_id)

        return channels_n_invite
