import torch
import time

class RobustPGDAttacker():
    def __init__(self, samp_num, trans,
        radius, steps, step_size, random_start, ascending=True):
        self.samp_num     = samp_num
        self.trans        = trans

        self.radius       = radius / 255.
        self.steps        = steps
        self.step_size    = step_size / 255.
        self.random_start = random_start
        self.ascending    = ascending

    def perturb(self, model, criterion, x, y):
        ''' initialize noise '''
        delta = torch.zeros_like(x.data)
        if self.steps==0 or self.radius==0:
            return delta

        if self.random_start:
            delta.uniform_(-self.radius, self.radius)

        ''' temporarily shutdown autograd of model to improve pgd efficiency '''
        model.eval()
        for pp in model.parameters():
            pp.requires_grad = False

        delta.requires_grad_()
        for step in range(self.steps):
            delta.grad = None

            for i in range(self.samp_num):
                adv_x = self.trans( (x + delta * 255).clamp(0., 255.) )
                _y = model(adv_x)
                lo = criterion(_y, y)
                lo.backward()

            with torch.no_grad():
                grad = delta.grad.data
                if not self.ascending: grad.mul_(-1)
                delta.add_(torch.sign(grad), alpha=self.step_size)
                delta.clamp_(-self.radius, self.radius)

        ''' reopen autograd of model after pgd '''
        for pp in model.parameters():
            pp.requires_grad = True

        return delta.data

#
# class RobustMinimaxPGDDefender():
#     def __init__(self, samp_num, trans,
#         radius, steps, step_size, random_start,
#         atk_radius, atk_steps, atk_step_size, atk_random_start,attacker):
#         self.samp_num         = samp_num
#         self.trans            = trans
#
#         self.radius           = radius / 255.
#         self.steps            = steps
#         self.step_size        = step_size / 255.
#         self.random_start     = random_start
#
#         self.atk_radius       = atk_radius / 255.
#         self.atk_steps        = atk_steps
#         self.atk_step_size    = atk_step_size / 255.
#         self.atk_random_start = atk_random_start
#         self.attacker  = attacker
#
#     def perturb(self, model, criterion, x, y):
#         ''' initialize noise '''
#         delta = torch.zeros_like(x)
#         if self.steps==0 or self.radius==0:
#             return delta
#
#         if self.random_start:
#             delta.uniform_(-self.radius, self.radius)
#
#         ''' temporarily disable autograd of model to improve pgd efficiency '''
#         model.eval()
#         for pp in model.parameters():
#             pp.requires_grad = False
#
#         delta.requires_grad_()
#         for step in range(self.steps):
#             delta.grad = None
#
#             for i in range(self.samp_num):
#                 def_x = self.trans( (x + delta * 255).clamp(0., 255.) )
#                 adv_x = self._get_adv_(model, criterion, def_x.data, y)
#
#                 adv_x.requires_grad_()
#                 _y = model(adv_x)
#                 lo = criterion(_y, y)
#
#                 gd = torch.autograd.grad(lo, [adv_x])[0]
#
#                 upd_lo = (def_x * gd).sum()
#                 upd_lo.backward()
#
#             with torch.no_grad():
#                 grad = delta.grad.data
#                 grad.mul_(-1)
#                 delta.add_(torch.sign(grad), alpha=self.step_size)
#                 delta.clamp_(-self.radius, self.radius)
#
#         ''' re-enable autograd of model after pgd '''
#         for pp in model.parameters():
#             pp.requires_grad = True
#
#         return delta.data
#
#     def _get_adv_(self, model, criterion, x, y):
#         return self.attacker.perturb(model,criterion,x,y)
#         # adv_x = x.clone()
#         # if self.atk_steps==0 or self.atk_radius==0:
#         #     return adv_x
#         #
#         # if self.atk_random_start:
#         #     adv_x += 2 * (torch.rand_like(x) - 0.5) * self.atk_radius
#         #     self._clip_(adv_x, x, radius=self.atk_radius)
#         #
#         # for step in range(self.atk_steps):
#         #     adv_x.requires_grad_()
#         #     _y = model(adv_x)
#         #     loss = criterion(_y, y)
#         #
#         #     ''' gradient ascent '''
#         #     grad = torch.autograd.grad(loss, [adv_x])[0]
#         #
#         #     with torch.no_grad():
#         #         adv_x.add_(torch.sign(grad), alpha=self.atk_step_size)
#         #         self._clip_(adv_x, x, radius=self.atk_radius)
#         #
#         # return adv_x.data
#
#     def _clip_(self, adv_x, x, radius):
#         adv_x -= x
#         adv_x.clamp_(-radius, radius)
#         adv_x += x
#         adv_x.clamp_(-0.5, 0.5)


class RobustMiniPGDAttackDefender():
    def __init__(self, samp_num, trans,
        radius, steps, step_size, random_start,
        atk_radius, atk_steps, atk_step_size, atk_random_start, attacker, uniform_scale=1.0):
        self.samp_num         = samp_num
        self.trans            = trans

        self.radius           = radius / 255.
        self.steps            = steps
        self.step_size        = step_size / 255.
        self.random_start     = random_start

        self.atk_radius       = atk_radius / 255.
        self.atk_steps        = atk_steps
        self.atk_step_size    = atk_step_size / 255.
        self.atk_random_start = atk_random_start
        self.uniform_scale = uniform_scale
        self.attacker = attacker

    def perturb(self, model, criterion, x, y):
        ''' initialize noise '''
        delta = torch.zeros_like(x)
        if self.steps==0 or self.radius==0:
            return delta

        if self.random_start:
            delta.uniform_(-self.radius, self.radius)

        ''' temporarily disable autograd of model to improve pgd efficiency '''
        model.eval()
        for pp in model.parameters():
            pp.requires_grad = False

        delta.requires_grad_()
        for step in range(self.steps):
            delta.grad = None
            s1 = time.time()
            for i in range(self.samp_num):
                s3 = time.time()
                def_x = self.trans( (x + delta * 255).clamp(0., 255.) )
                adv_x = self._get_adv_(model, criterion, def_x.data, y) # 找对抗噪声

                adv_x.requires_grad_()
                _y = model(adv_x)
                lo = criterion(_y, y)

                gd = torch.autograd.grad(lo, [adv_x])[0]

                upd_lo = (def_x * gd).sum()
                upd_lo.backward()
                s4 = time.time()
                # print(f"{s4-s3}s to conduct one attack sample!")

            with torch.no_grad():
                grad = delta.grad.data
                grad.mul_(-1)
                delta.add_(torch.sign(grad), alpha=self.step_size)
                delta.clamp_(-self.radius, self.radius)

            s2 = time.time()
            # print(f"{s2-s1}s to conduct one step defense noise training!")
            

        ''' re-enable autograd of model after pgd '''
        for pp in model.parameters():
            pp.requires_grad = True

        return delta.data

    def _get_adv_(self, model, criterion, x, y):
        # return self.attacker.perturb(model,criterion,x,y)
        adv_x = x.clone()
        if self.atk_steps == 0 or self.atk_radius == 0:
            return adv_x

        if self.atk_random_start:
            adv_x += 2 * (torch.rand_like(x) - 0.5) * self.atk_radius
            self._clip_(adv_x, x, radius=self.atk_radius)

        ''' temporarily shutdown autograd of model to improve pgd efficiency '''
        model.eval()
        for pp in model.parameters():
            pp.requires_grad = False

        for step in range(self.atk_steps):
            adv_x.requires_grad_()
            _y = model(adv_x)
            loss = criterion(_y, y)

            ''' gradient ascent '''
            grad = torch.autograd.grad(loss, [adv_x])[0]

            with torch.no_grad():
                adv_x.add_(torch.sign(grad), alpha=self.atk_step_size)
                self._clip_(adv_x, x, radius=self.atk_radius)

        ''' reopen autograd of model after pgd '''
        for pp in model.parameters():
            pp.requires_grad = True
            
        return adv_x.data

    def _get_adv_random_(self, model, criterion, x, y):
        adv_x = x.clone()
        if self.atk_steps == 0 or self.atk_radius == 0:
            return adv_x

        if self.atk_random_start:
            adv_x += 2 * (torch.rand_like(x) - 0.5) * self.atk_radius
            self._clip_(adv_x, x, radius=self.atk_radius)
        return adv_x.data

    def _clip_(self, adv_x, x, radius):
        adv_x -= x
        adv_x.clamp_(-radius, radius)
        adv_x += x
        adv_x.clamp_(-0.5, 0.5)

