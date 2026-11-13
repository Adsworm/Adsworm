import sys, warnings; warnings.filterwarnings('ignore')
from clearvoice import ClearVoice
cv = ClearVoice(task='speech_enhancement', model_names=['MossFormer2_SE_48K'])
out = cv(input_path=sys.argv[1], online_write=False); cv.write(out, output_path=sys.argv[2]); print('wrote', sys.argv[2])
