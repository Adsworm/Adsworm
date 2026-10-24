"""Face landmarks + multiclass segmentation for a portrait -> npz (pts, fg, hair, face, body)."""
import sys, numpy as np, cv2, mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision


def guided(I, p, r, eps):
    """He et al. guided filter, grey guide in [0,1]."""
    box = lambda x: cv2.blur(x, (2 * r + 1, 2 * r + 1))
    mI, mp_ = box(I), box(p)
    a = (box(I * p) - mI * mp_) / (box(I * I) - mI * mI + eps)
    b = mp_ - a * mI
    return box(a) * I + box(b)


src, out = sys.argv[1], sys.argv[2]
rgb = cv2.cvtColor(cv2.imread(src, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
h, w = rgb.shape[:2]
W = 1600
small = np.ascontiguousarray(cv2.resize(rgb, (W, int(W * h / w)), interpolation=cv2.INTER_AREA))
img = mp.Image(image_format=mp.ImageFormat.SRGB, data=small)

lm = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
    base_options=mpt.BaseOptions(model_asset_path='models/face_landmarker.task'), num_faces=1))
pts = np.array([[p.x * w, p.y * h, p.z * w] for p in lm.detect(img).face_landmarks[0]], np.float32)

seg = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
    base_options=mpt.BaseOptions(model_asset_path='models/selfie_multiclass_256x256.tflite'),
    output_category_mask=True))
cat = np.squeeze(seg.segment(img).category_mask.numpy_view())  # 0 bg 1 hair 2 body 3 face 4 clothes 5 other
gray = cv2.cvtColor(small, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255
masks = {}
for name, ids in dict(fg=(1, 2, 3, 4, 5), hair=(1,), face=(3,), body=(2,), clothes=(4,)).items():
    m = np.isin(cat, ids).astype(np.float32)
    m = np.clip(guided(gray, m, 6, 1e-3), 0, 1)
    masks[name] = cv2.resize(m, (w, h), interpolation=cv2.INTER_CUBIC).clip(0, 1).astype(np.float16)
np.savez_compressed(out, pts=pts, **masks)

dbg = (small * 0.45).astype(np.float32)
fg = cv2.resize(masks['fg'].astype(np.float32), (W, small.shape[0]))
hair = cv2.resize(masks['hair'].astype(np.float32), (W, small.shape[0]))
dbg[..., 1] += hair * 120
dbg[..., 2] += (fg - hair).clip(0, 1) * 80
for x, y, _ in pts:
    cv2.circle(dbg, (int(x * W / w), int(y * W / w)), 2, (255, 255, 0), -1)
cv2.imwrite(out.replace('.npz', '_dbg.jpg'), cv2.cvtColor(cv2.resize(dbg.clip(0, 255).astype(np.uint8), (800, int(800 * h / w))), cv2.COLOR_RGB2BGR))
print('ok', w, h)
