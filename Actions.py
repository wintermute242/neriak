import Timer, GameInput

class AvatarSwapping:
    _trigger_swap_to_primary = 'Your body screams with the power of an Avatar'
    _avatar_refresh_timer = 230 # Seconds
    _has_avatar_buff = False

    def __init__(avatar_bandolier_key, primary_bandolier_key):
        _avatar_key = avatar_bandolier_key
        _primary_key = primary_bandolier_key
        _clock = Timer.Timer()
        _clock.set_alarm(AvatarSwapping._avatar_refresh_timer)

    def Get_Triggers():
        return [AvatarSwapping._trigger_swap_to_primary]

    def Handle_Event(event=None):
        if AvatarSwapping._has_avatar_buff:
            GameInput.send(AvatarSwapping._avatar_key)
        
        else:
            AvatarSwapping._clock.start()
            GameInput.send(AvatarSwapping._primary_bandolier_key)

    def Update(update=None):
        if AvatarSwapping._clock.alarmed():
            AvatarSwapping._clock.reset()
            AvatarSwapping.Handle_Event()

