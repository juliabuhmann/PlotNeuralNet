import sys

sys.path.append('../')
from pycore.tikzeng import *
from pycore.blocks import *

shapes = [(42, 430, 430), (38, 142, 142), (34, 46, 46), (10, 14, 14),
          (14, 26, 26), (10, 74, 74), (6, 218, 218)]

dh_unet = True

if dh_unet:
    offset_mask = 2.5
    offset_dir = -offset_mask
else:
    offset_mask = 0
    offset_dir = 0

arch = [
    to_head('..'),
    to_cor(),
    to_begin(),

    to_3DBox(name='raw', offset="(-2,0,0)", to="(-2,0,0)", width=42, height=430,
             depth=430, fill='\RawBox'),

    # input
    to_input('pictures/raw_model.png', 'raw-east'),
    #
    # block-001
    to_3DBox(name='b1', offset="(0,0,0)", to="(0,0,0)", width=42, height=430,
             depth=430),

    *block_3DBox(name='b2', botton='b1', offset="(2, 0, 0)", size=shapes[1]),
    *block_3DBox(name='b3', botton='b2', offset="(2, 0, 0)", size=shapes[2]),

    # bottleneck
    *block_3DBox(name='b4', botton='b3', offset="(2, 0, 0)", size=shapes[3]),

    # Upsampling Path
    *block_3DBox(name='u4', botton='b4', offset=f"(2, {offset_mask}, 0)",
                 size=shapes[4]),
    to_skip('b3', 'u4', pos=1.25),

    *block_3DBox(name='u5', botton='u4', offset=f"(2, 0, 0)",
                 size=shapes[5]),
    to_skip('b2', 'u5', pos=1.25),

    *block_3DBox(name='u6', botton='u5', offset=f"(2, 0, 0)",
                 size=shapes[6]),
    to_skip('b1', 'u6', pos=1.25),

    to_3DBox(name='m_out', offset="(2,0,0)", to="(u6-east)",
             width=shapes[6][0], height=shapes[6][2],
             depth=shapes[6][1], fill='\RawBox'),

    to_input(
        'pictures/predictions_m_pred.png',
        to='m_out-east', width=4, height=4),
]

dir_path = [
    *block_3DBox(name='u4_d', botton='b4', offset=f"(2, {offset_dir}, 0)",
                 size=shapes[4]),
    to_skip_south('b3', 'u4_d', pos=1.25),

    *block_3DBox(name='u5_d', botton='u4_d', offset=f"(2, 0, 0)",
                 size=shapes[5]),
    to_skip_south('b2', 'u5_d', pos=1.25),

    *block_3DBox(name='u6_d', botton='u5_d', offset=f"(2, 0, 0)",
                 size=shapes[6]),
    to_skip_south('b1', 'u6_d', pos=1.25),

    to_3DBox(name='d_out', offset="(2,0,0)", to="(u6_d-east)",
             width=shapes[6][0], height=shapes[6][2],
             depth=shapes[6][1], fill='\RawBox'),

    to_input('pictures/d_model.png',
             to='d_out-east', width=4, height=4),

]
arch.extend(dir_path)
arch.append(to_end())


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex')


if __name__ == '__main__':
    main()
