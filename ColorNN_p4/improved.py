import gradient as gr
import numpy as np
import matplotlib.pyplot as plt
import patch as p
import gray as g
from numpy.random import default_rng

class improved_agent:

        def __init__(self, img_path, alpha):
                self.img_path = img_path
                self.alpha = alpha
                self.rng = default_rng()
                self.clr_img = np.array(plt.imread(self.img_path))
                self.gray_img = g.color_to_gray(self.img_path)
                print('Start')
                self.red_model = self.build_model(0)
                self.green_model = self.build_model(1)
                self.blue_model = self.build_model(2)

        def build_model(self, r_g_b_ind):
                rows, cols, _ = self.clr_img.shape
                w_t = np.zeros(51)
                w_tplus = np.full(51, 1)
                i = 1
                L_inc = 0
                losses = []
                chang = []
                time = []
                s = 0
                self.alpha = .1
                iterr = 100000000
                while i < iterr and (len(losses)<=1 or losses[-1]>10) and self.alpha > .005:
                        #calculating new weights
                        w_t = np.array(w_tplus)
                        #r = self.rng.integers(1, high=rows-1)
                        #c = self.rng.integers(1, high=(cols // 2))
                        r = self.rng.integers(2, high=rows-2)
                        c = self.rng.integers(2, high=(cols // 2)-1)
                        #print("Chose", r, c)
                        x = p.build_big_patch(self.gray_img, r, c)
                        x = [((np.max(a)) / 255) for a in x ]
                        #x = [(np.array(x).mean() - 128) / 255]
                        #print(x)
                        x.insert(0, 1)
                        #print(x)
                        x = np.array(x)
                        x = np.append(x,x[1:]**2)
                        y = self.clr_img[r][c][r_g_b_ind]
                        y = y / 255
                        #print(w_t)
                        w_tplus = gr.w_tplus(w_t, x, y, self.alpha)
                        #print(w_tplus)
                        #print(w_tplus - w_t)
                        if (w_tplus - w_t).sum() == 0:
                                print("No change")
                        #else:
                        #       print((w_tplus - w_t).sum())
                        #input()

                        #checking loss
                        r = self.rng.integers(2, high=rows-2)
                        c = self.rng.integers(2, high=(cols // 2)-1)
                        x = p.build_big_patch(self.gray_img, r, c)
                        x = [((np.max(a)) / 255) for a in x ]
                        #x = [(np.array(x).mean() - 128) / 255]
                        x.insert(0, 1)
                        x = np.array(x)
                        x = np.append(x,x[1:]**2)
                        y = self.clr_img[r][c][r_g_b_ind]
                        y = y / 255
                        #old_loss = gr.L(w_t, x, y)
                        new_loss = gr.L(w_tplus, x, y)
                        s += new_loss
                        if i % (5000) == 0:
                                if len(losses) > 2 and abs(losses[-1]-losses[-2]) < .5:
                                        self.alpha*=.8
                                        print(self.alpha)
                                s/=5000
                                losses.append(s)
                                s = 0
                                print((losses[-1]))
                                print(w_tplus)
                        if i % 30000 == 0 and i >= 60000:
                                time.append(i / 300000)
                                chang.append(losses[-1])
                                #plt.scatter(time, chang)
                                #plt.show()
                        i += 1
                        #print("Iteration", i, "complete.")
                print("Done building model", r_g_b_ind)
                #input()
                return w_tplus

        def run(self):
                rows, cols, _ = self.clr_img.shape
                div_line = cols // 2
                for row in range(rows):
                        if row == 0 or row == 1 or row == rows-2 or row == rows-1:
                                continue
                        col = div_line+5
                        while col < cols - 5:
                                try:
                                        x = p.build_big_patch(self.gray_img, row, col)
                                except:
                                        print([row,col])
                                        input()
                                x = [(np.max(a))/255 for a in x ]
                                x.insert(0, 1)
                                x = np.array(x)
                                x = np.append(x,x[1:]**2)
                                r = int(round(gr.sigmoid(np.dot(self.red_model, x))*255))
                                g = int(round(gr.sigmoid(np.dot(self.green_model, x))*255))
                                b = int(round(gr.sigmoid(np.dot(self.blue_model, x))*255))
                                #print([r,g,b])
                                #input()
                                self.clr_img[row][col] = np.array([r,g,b])
                                col += 1
                                #print("Colored pixel", row, ",", col)
                        #print("Progress", row / rows)
                plt.imshow(self.clr_img)
                plt.show()
                return self.clr_img


impr_agent = improved_agent("mountains.jpg", .1)
impr_agent.run()
