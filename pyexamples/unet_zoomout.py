import sys
import numpy as np

sys.path.append('../')
from pycore.tikzeng import *
from pycore.blocks import *

shapes = [(42, 430, 430), (38, 142, 142), (34, 46, 46), (10, 14, 14),
          (14, 26, 26), (10, 74, 74), (6, 218, 218)]

voxel_size = np.array((40, 4, 4))

in_nm = False
scale = 0.1
if in_nm:
    shapes = [np.array(shape)*voxel_size for shape in shapes]
    scale = 0.025

modeltype = 'ST_m'
modeltype = 'MT1'


outputimage = 'predictions_m_pred'
if modeltype == 'MT2':
    offset_mask = 2.5
    offset_dir = -offset_mask

else:
    offset_mask = 0
    offset_dir = 0
if modeltype == 'ST_d':
    outputimage = 'd_model'

arch = [
    to_head('..'),
    to_cor(),
    to_begin(),

    to_3DBox(name='raw', offset="(-2,0,0)", to="(-2,0,0)", width=shapes[0][0], height=shapes[0][1],
             depth=shapes[0][2], fill='\RawBox', scale=scale),

    # input
    to_input('pictures/raw_model.png', 'raw-east', height=80*scale, width=80*scale),
    #
    # block-001
    to_3DBox(name='b1', offset="(0,0,0)", to="(0,0,0)", width=shapes[0][0], height=shapes[0][1],
             depth=shapes[0][2], scale=scale),

    *block_3DBox(name='b2', botton='b1', offset="(2, 0, 0)", size=shapes[1], scale=scale),
    *block_3DBox(name='b3', botton='b2', offset="(2, 0, 0)", size=shapes[2], scale=scale),

    # bottleneck
    *block_3DBox(name='b4', botton='b3', offset="(2, 0, 0)", size=shapes[3], scale=scale),
    ]

m_path = [
    # Upsampling Path
    *block_3DBox(name='u4', botton='b4', offset=f"(2, {offset_mask}, 0)",
                 size=shapes[4], scale=scale),
    to_skip('b3', 'u4', pos=1.25),

    *block_3DBox(name='u5', botton='u4', offset=f"(2, 0, 0)",
                 size=shapes[5], scale=scale),
    to_skip('b2', 'u5', pos=1.25),

    *block_3DBox(name='u6', botton='u5', offset=f"(2, 0, 0)",
                 size=shapes[6], scale=scale),
    to_skip('b1', 'u6', pos=1.25),
]

main_output = [
    to_3DBox(name='m_out', offset="(2,0,0)", to="(u6-east)",
             width=shapes[6][0], height=shapes[6][2],
             depth=shapes[6][1], fill='\RawBox', scale=scale),

    to_input(
        f'pictures/{outputimage}.png',
        to='m_out-east', width=40*scale, height=40*scale),
]

mt1_output = [
    to_3DBox(name='m_out', offset="(2,3,0)", to="(u6-east)",
             width=shapes[6][0], height=shapes[6][2],
             depth=shapes[6][1], fill='\RawBox', scale=scale),

    to_input(
        f'pictures/{outputimage}.png',
        to='m_out-east', width=40*scale, height=40*scale),

    to_3DBox(name='d_out', offset="(2,-3,0)", to="(u6-east)",
             width=shapes[6][0], height=shapes[6][2],
             depth=shapes[6][1], fill='\RawBox', scale=scale),

    to_input('pictures/d_model.png',
             to='d_out-east', width=40*scale, height=40*scale),

]

dir_path = [
    *block_3DBox(name='u4_d', botton='b4', offset=f"(2, {offset_dir}, 0)",
                 size=shapes[4], scale=scale),
    to_skip_south('b3', 'u4_d', pos=1.25),

    *block_3DBox(name='u5_d', botton='u4_d', offset=f"(2, 0, 0)",
                 size=shapes[5], scale=scale),
    to_skip_south('b2', 'u5_d', pos=1.25),

    *block_3DBox(name='u6_d', botton='u5_d', offset=f"(2, 0, 0)",
                 size=shapes[6], scale=scale),
    to_skip_south('b1', 'u6_d', pos=1.25),

    to_3DBox(name='d_out', offset="(2,0,0)", to="(u6_d-east)",
             width=shapes[6][0], height=shapes[6][2],
             depth=shapes[6][1], fill='\RawBox', scale=scale),

    to_input('pictures/d_model.png',
             to='d_out-east', width=40*scale, height=4*scale),

]
# if not modeltype == 'ST_d':
arch.extend(m_path)
if modeltype == 'MT1':
    arch.extend(mt1_output)
else:
    arch.extend(main_output)

if modeltype == 'MT2':
    arch.extend(dir_path)
arch.append(to_end())


def main():
    to_generate(arch, modeltype + '.tex')


if __name__ == '__main__':
    main()
