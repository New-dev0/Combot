class AlreadyParticipated(Exception):
    ...


class NoWarnsFound(Exception):
    ...


class IntializeCommunity:
    def __init__(self, community_id: str):
        self.community_id = community_id
        self.warns = {}

        from bot import DB

        self.db = DB
        self._com = self.db.child(self.community_id)

    # Welcome Stuffs
    async def get_welcome(self):
        return self._com.child("welcome_db").get()

    async def set_welcome(
        self,
        text: str,
        notify_channel_id: str,
        is_group: bool = True,
        stuffs: dict = None,
        verify: bool = False,
    ):
        data = {
            "text": text,
            "notify_channel_id": notify_channel_id,
            "is_group": is_group,
            "stuffs": stuffs,
            "verify": verify,
        }
        return self._com.child("welcome_db").set(data)

    def delete_welcome(self):
        self._com.child("welcome_db").delete()

    async def update_welcome(
        self,
        text: str = None,
        notify_channel_id: str = None,
        is_group: bool = None,
        stuffs: dict = None,
    ):
        data = {}
        if text:
            data["text"] = text
        if notify_channel_id:
            data["notify_channel_id"] = notify_channel_id
        if is_group is not None:
            data["is_group"] = is_group
        if stuffs:
            data["stuffs"] = stuffs
        return self._com.child("welcome_db").update(data)

    # GiveAway Settings

    async def add_giveaway(
        self,
        reaward_text: str,
        giveaway_id: str,
        giveaway_title: str,
        winner_count: int,
    ):
        data = {
            "reaward_text": reaward_text,
            "giveaway_title": giveaway_title,
            "winner_count": winner_count,
        }
        return self._com.child(f"giveaway_db/{giveaway_id}").set(data)

    async def get_giveaways(self, giveaway_id: str = None):
        if not giveaway_id:
            return await self.db.read_data(f"{self.community_id}/giveaway_db/")
        return self.db.child(f"{self.community_id}/giveaway_db/{giveaway_id}/").get()

    async def get_participants_from_giveaway(self, giveaway_id):
        return self.db.child(
            f"{self.community_id}/giveaway_db/{giveaway_id}/participants/"
        ).get()

    async def add_participant_in_giveaway(self, giveaway_id, user_id):
        data = self.db.child(f"{self.community_id}/giveaway_db/{giveaway_id}/").get()
        par = data.get("participants") or []
        if user_id in par:
            raise AlreadyParticipated(f"{user_id} Is Already Paricipated In GiveAway!")
        par.append(user_id)
        data["participants"] = par
        return await self.db.child(
            f"{self.community_id}/giveaway_db/{giveaway_id}/"
        ).set(data)

    async def delete_giveaway(self, giveaway_id):
        return await self.db.child(
            f"{self.community_id}/giveaway_db/{giveaway_id}/"
        ).delete()

    # Warn Settings

    async def add_warns(self, user_id, count: int = 1, reason=None):
        data = await self.db.read_data(f"{self.community_id}/warn_db/{user_id}/") or {}
        if data:
            data["count"] += count
            data["reason"] = reason or "No Reason Where Given!"
            return await self.db.update_data(
                f"{self.community_id}/warn_db/{user_id}/", data
            )
        data["count"] = count
        data["reason"] = reason or "No Reason Where Given!"
        return self._com.child(f"/warn_db/{user_id}/").set(data)

    async def get_warns(self, user_id):
        data = self.db.child(f"{self.community_id}/warn_db/{user_id}/").get()
        if data:
            return data
        raise NoWarnsFound("No Warns Found On Given User!")

    async def reset_warns(self, user_id):
        return self.db.child(f"{self.community_id}/warn_db/{user_id}/").delete()

    @property
    def economy(self):
        return self._com.child("economy").get()

    def user(self, user_id):
        return self._com.child("Users").child(str(user_id))

    def get_user_credit(self, user_id):
        user_id = str(user_id)
        user = self._com.child("Users").child(user_id)
        data = user.get()
        if data is None:
            data = {"credits": 40}
            user.set(data)
        return data.get("credits", 0)

    def reduce_economy_credit(self, user_id, credit):
        user_id = str(user_id)
        if not self._com.child("economy").get():
            return
        user = self._com.child("Users").child(user_id)
        data = user.get() or {}
        if "credits" in data:
            credit = data["credits"] - credit
            credit = max(credit, 0)
            data["credits"] = credit
            user.set(data)
        return

    def add_economy_credit(self, user_id, credit):
        user_id = str(user_id)
        if not self._com.child("economy").get():
            return
        user = self._com.child("Users").child(user_id)
        data = user.get() or {}
        if "credits" not in data:
            data["credits"] = 40 + credit
        else:
            data["credits"] += credit
        user.set(data)
        return True
