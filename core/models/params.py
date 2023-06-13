null_blank = {"null": True, "blank": True}
null_blank_8 = {"null": True, "blank": True, "max_length": 8}
null_blank_16 = {"null": True, "blank": True, "max_length": 16}
null_blank_32 = {"null": True, "blank": True, "max_length": 32}
null_blank_64 = {"null": True, "blank": True, "max_length": 34}
null_blank_128 = {"null": True, "blank": True, "max_length": 128}
null_blank_256 = {"null": True, "blank": True, "max_length": 256}
null_blank_528 = {"null": True, "blank": True, "max_length": 528}
null_blank_1024 = {"null": True, "blank": True, "max_length": 1024}
null_blank_2048 = {"null": True, "blank": True, "max_length": 2048}

null_16 = {"null": True, "max_length": 16}
null_32 = {"null": True, "max_length": 32}
null_64 = {"null": True, "max_length": 34}
null_128 = {"null": True, "max_length": 128}
null_256 = {"null": True, "max_length": 256}
null_528 = {"null": True, "max_length": 528}
null_1024 = {"null": True, "max_length": 1024}
null_2048 = {"null": True, "max_length": 2048}


def profile_photo_upload_path(profile, filename):
    return f"profiles/{profile.category}/{profile.id}/photos/{filename}"


def cv_upload_path(cv, filename):
    return f"profiles/{cv.profile.category}/{cv.profile.id}/cvs/{filename}"
