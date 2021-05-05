from PIL import Image
im1 = Image.open(r'quad.png')
rgb_im = im1.convert('RGB')
rgb_im.save(r'imp_quad.jpg')