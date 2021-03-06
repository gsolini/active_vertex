from voronoi_model.voronoi_model_periodic import *
import numpy as np
import matplotlib.pyplot as plt


vor = Tissue()
vor.generate_cells(600)
vor.make_init_balanced(9,noise = 0.0005)

p0 = 3.8333333333333335
r = 5
vor.v0 = 0.06833333
vor.Dr = 1e-1
beta = 0.05994843

vor.kappa_A = 1
vor.kappa_P = 1/r
vor.A0 = 1
vor.P0 = p0
vor.a = 0.3
vor.k = 1

vor.set_interaction(W = (2*beta*vor.P0/r)*np.array([[0, 1], [1, 0]]),pE=0.5,randomize=False)


vor.set_t_span(0.025,100)

vor.simulate()
vor.plot_scatter = False


nt = 4
t_range = np.linspace(0,vor.t_span.size-1,nt).astype(np.int64)
fig, ax = plt.subplots(1,nt)
for i, t in enumerate(t_range):
    vor.plot_vor(vor.x_save[t],ax[i])
    ax[i].axis("off")
fig.show()

vor.animate(n_frames=30)



#
#
# prop = 0.5
# p0eff = p0*(1-prop*vor.J.max()/(vor.P0*vor.kappa_P))
#
#
#
# shape_index = vor.P/np.sqrt(vor.A)
# fig, ax = plt.subplots()
# ax.hist(shape_index)
# fig.show()
# print(shape_index.mean())
#
# vor.get_self_self_interface(100)
# nA,nB = vor.get_num_islands(100)
#
# fig, ax = plt.subplots(1,2)
# ax[0].plot(vor.self_self_interface.mean(axis=1))
# ax[1].plot(nA)
# ax[1].plot(nB)
# fig.show()
#
#
# #
# # fig, ax = plt.subplots()
# # vor.plot_vor(vor.x_save[93],ax)
# # ax.axis("off")
# # fig.show()
#
#
# #
# def image(x,L,res=25):
#     X,Y = np.meshgrid(np.linspace(0,L,res),np.linspace(0,L,res),indexing="ij")
#     XX,YY = X.ravel(),Y.ravel()
#     d = (np.mod(np.outer(XX, np.ones_like(x[:, 0])) - np.outer(np.ones_like(XX), x[:, 0]) + L / 2, L) - L / 2) ** 2 + (np.mod(np.outer(YY, np.ones_like(x[:, 1])) - np.outer(np.ones_like(XX), x[:, 1]) + L / 2, L)- L / 2) ** 2
#     im = np.empty(XX.shape,dtype=np.int32)
#     for i, D in enumerate(d):
#         im[i] = np.argmin(D)
#     im = im.reshape(X.shape)
#     return im
#
# def type_im(x,L,c_types,res=25):
#     im = image(x,L,res=res)
#     tim = c_types[im]
#     return tim
#
# @jit(nopython=True,cache=True)
# def type_im_fast(XX,YY,res,x,L,c_types):
#     d = (np.mod(np.outer(XX, np.ones_like(x[:, 0])) - np.outer(np.ones_like(XX), x[:, 0]) + L / 2, L) - L / 2) ** 2 + (np.mod(np.outer(YY, np.ones_like(x[:, 1])) - np.outer(np.ones_like(XX), x[:, 1]) + L / 2, L)- L / 2) ** 2
#     im = np.empty(XX.shape, dtype=np.int32)
#     for i, D in enumerate(d):
#         im[i] = np.argmin(D)
#     im = im.reshape((res,res))
#     tim = c_types[im.ravel()].reshape((res,res))
#     return tim
#
# @jit(nopython=True,cache=True)
# def get_radial_profile(X,Y,res,x,L,c_types,Dround):
#     tim = type_im_fast(X.ravel(), Y.ravel(), res, x, L, c_types)
#     tim = 2 * tim - 1
#     val = np.outer(tim.ravel(), np.ones_like(tim.ravel())) * np.outer(np.ones_like(tim.ravel()), tim.ravel())
#     tbin = np.bincount(Dround.ravel(), val.ravel())
#     nr = np.bincount(Dround.ravel())
#     radialprofile = tbin / nr
#     return radialprofile
#
# @jit(nopython=True,cache=True)
# def get_radial_profile_type(X,Y,res,x,L,c_types,Dround,ctype=0):
#     """
#     Radial profile but for a specific cell type
#     :param X:
#     :param Y:
#     :param res:
#     :param x:
#     :param L:
#     :param c_types:
#     :param Dround:
#     :param ctype:
#     :return:
#     """
#     tim = type_im_fast(X.ravel(), Y.ravel(), res, x, L, c_types)
#     type_mask = (tim==ctype).ravel()
#     tim = 2 * tim - 1
#     val = np.outer(tim.ravel()[type_mask], np.ones_like(tim.ravel())) * np.outer(np.ones(type_mask.sum()), tim.ravel())
#     tbin = np.bincount(Dround[type_mask].ravel(), val.ravel())
#     nr = np.bincount(Dround[type_mask].ravel())
#     radialprofile = tbin / nr
#     return radialprofile
#
# @jit(nopython=True,cache=True)
# def get_radial_profile_type_norm(X,Y,res,x,L,c_types,Dround):
#     """
#     Radial profile, normalized by the numbers of each cell type (or rather the number of occupied pixels)
#
#     This counteracts artefact in autocorrelation where self-self > 0 as x --> infinity due to unequal cell numbers.
#     :param X:
#     :param Y:
#     :param res:
#     :param x:
#     :param L:
#     :param c_types:
#     :param Dround:
#     :return:
#     """
#     tim = type_im_fast(X.ravel(), Y.ravel(), res, x, L, c_types)
#     type_mask = (tim==0).ravel()
#     tim = 2 * tim - 1
#     val = np.outer(tim.ravel()[type_mask], np.ones_like(tim.ravel())) * np.outer(np.ones(type_mask.sum()), tim.ravel())
#     tbin = np.bincount(Dround[type_mask].ravel(), val.ravel())
#     nr = np.bincount(Dround[type_mask].ravel())
#     radialprofileA = tbin / nr
#     val = np.outer(tim.ravel()[~type_mask], np.ones_like(tim.ravel())) * np.outer(np.ones((~type_mask).sum()), tim.ravel())
#     tbin = np.bincount(Dround[~type_mask].ravel(), val.ravel())
#     nr = np.bincount(Dround[~type_mask].ravel())
#     radialprofileB = tbin / nr
#     return (radialprofileA + radialprofileB)/2
#
# def get_radial_profiles(x_save,skip,mult,L,c_types,res):
#     x_range = (np.arange(res)+0.5)/res*L
#     X,Y = np.meshgrid(x_range,x_range,indexing="ij")
#     dX = np.outer(X.ravel(), np.ones_like(X.ravel())) - np.outer(np.ones_like(X.ravel()), X.ravel())
#     dY = np.outer(Y.ravel(), np.ones_like(Y.ravel())) - np.outer(np.ones_like(Y.ravel()), Y.ravel())
#     dX, dY = np.mod(dX + L / 2, L) - L / 2, np.mod(dY + L / 2, L) - L / 2
#     D = np.sqrt(dX ** 2 + dY ** 2)
#     Dround = (D * mult).astype(int)
#     ds = np.unique(Dround.ravel()) / mult
#
#     radialprofiles = np.zeros((x_save[::skip].shape[0],np.amax(Dround)+1))
#     for i, x in enumerate(x_save[::skip]):
#         radialprofiles[i]=  get_radial_profile(X, Y, res, x, L, c_types, Dround)
#     return radialprofiles,ds
#
# rad,ds = get_radial_profiles(vor.x_save,300,5,vor.L,vor.c_types,res=70)
# plt.imshow(rad.T,extent=[-1,1,-1,1],vmax=0.1,vmin=-0.1)
# plt.show()
# def get_radial_profiles_type(x_save,skip,mult,L,c_types,res):
#     x_range = (np.arange(res)+0.5)/res*L
#     X,Y = np.meshgrid(x_range,x_range,indexing="ij")
#     dX = np.outer(X.ravel(), np.ones_like(X.ravel())) - np.outer(np.ones_like(X.ravel()), X.ravel())
#     dY = np.outer(Y.ravel(), np.ones_like(Y.ravel())) - np.outer(np.ones_like(Y.ravel()), Y.ravel())
#     dX, dY = np.mod(dX + L / 2, L) - L / 2, np.mod(dY + L / 2, L) - L / 2
#     D = np.sqrt(dX ** 2 + dY ** 2)
#     Dround = (D * mult).astype(int)
#     Dmax = np.amax(Dround) + 1
#     ds = np.arange(Dmax)/mult
#
#     radialprofiles = np.zeros((x_save[::skip].shape[0],ds.size))
#     for i, x in enumerate(x_save[::skip]):
#         radialprofiles[i]=  get_radial_profile_type_norm(X, Y, res, x, L, c_types, Dround)
#     return radialprofiles,ds
#
# rad,ds = get_radial_profiles_type(vor.x_save,100,2,vor.L,vor.c_types,res=40)
# plt.imshow(rad.T,extent=[-1,1,-1,1],vmax=0.1,vmin=-0.1)
# plt.show()
#
# """
# Generates a contour plot for the radial distribution function
# """
#
# t_sel = vor.t_span[::100]
# TT, DD = np.meshgrid(t_sel,ds)
#
# levels = np.linspace(-0.05,0.05,100)
# rad_mod =rad.copy()
# rad_mod[rad<=levels.min()] = levels.min() +1e-17
# rad_mod[rad>=levels.max()] = levels.max() - 1e-17
#
# plt.tricontourf(TT.ravel(),DD.ravel(),(rad_mod.T).ravel(),levels=levels,cmap=plt.cm.plasma)
# plt.show()
#
#
#
# from scipy.optimize import curve_fit
#
# def corr_fn(r,a,b):
#     return np.exp(-a*r)*np.cos(r*np.pi*2/b)
#
# def get_L_star(x_save,skip,mult,L,c_types,res):
#     rads,ds = get_radial_profiles_type(x_save,skip,mult,L,c_types,res)
#     L_stars = np.zeros(rads.shape[0])
#     a,b = L,L
#     for i, rad in enumerate(rads):
#         mask = ~np.isnan(rad)
#         a,b = curve_fit(corr_fn, ds[mask],rad[mask],(a,b),bounds=(np.array([0,0]),np.array([np.inf,np.sqrt(2)*L])))[0]
#         L_stars[i] = b
#     return rads,L_stars
#
#
#
# for res in [20,30,40,50]:
#     rads,L_star = get_L_star(vor.x_save,100,20,vor.L,vor.c_types,res=res)
#     plt.plot(L_star)
# plt.show()
#
#
# rads,L_star = get_L_star(vor.x_save,50,10,vor.L,vor.c_types,res=30)
#
# fig, ax = plt.subplots(figsize=(4,4))
# ax.plot(L_star)
# ax.set(xlabel="Correlation lengthscale",ylabel="Time")
# fig.show()
#
# #
# # vor.animate(n_frames=50)
# #
# #
# # vor.get_self_self()
# # fig, ax = plt.subplots()
# # ax.plot(vor.self_self)
# # ax.set(xlabel="Time",ylabel="Fraction of self-self interactions")
# # fig.savefig("self_self.pdf")
# #
# #
# # ratio = 0.5
# # P0_eff = alpha*ratio/vor.kappa_P + vor.P0
# # p0_eff = P0_eff/np.sqrt(vor.A0)
# # print(p0_eff)
# #
# # """
# # Stat to measure q for each cell.
# # And compare with neighbourhood and thus p0_eff
# # And MSD (short time-scale)
# # """