def extract_vehicle_name(vehicle_code_name):
    input_split = vehicle_code_name.replace('ks_', '', 1).replace('_', ' ').split(' ', 1)
    make_name = input_split[0].title()
    model_name = input_split[1].title()
    return make_name, model_name


def extract_track_name(track_code_name):
    input_split = track_code_name.replace('ks_', '', 1).replace('_', ' ').replace('-layout', '-').split('-')
    track_name = input_split[0].strip().title()
    track_variant = input_split[1].strip().title() if len(input_split) > 1 else None
    return '{:s} - {:s}'.format(track_name, track_variant)
