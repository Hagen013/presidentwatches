
import { Message } from 'element-ui'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'

import router from '@/router'
import store from '@/store'
import { getToken, getRefreshToken } from '@/utils/auth' 


NProgress.configure({ showSpinner: false }) // NProgress Configuration

const whiteList = ['/login',] // no redirect whitelist


router.beforeEach(async(to, from, next) => {

    // start progress bar
    NProgress.start()
    
    const hasToken = getRefreshToken()

    if (hasToken) {
        next()
        if (to.path === '/login') {
            next({path: '/'})
            Progress.done()
        }
    } else {
        next()
        if (whiteList.indexOf(to.path) !== -1) {
            next()
        } else {
            next(`/login?redirect=${to.path}`)
            NProgress.done()
        }
    }

})
  
router.afterEach(() => {
    NProgress.done()
})
  