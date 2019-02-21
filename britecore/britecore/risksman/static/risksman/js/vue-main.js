new Vue({
      el: '#app',
 
    router: new VueRouter({
        linkExactActiveClass: 'active',
        routes: [
            {
                path: '/',
                component: Fields
            },
            
            {
                path: '/risks-types',
                component: RiskTypes
            },
            
            {
                path: '/risks',
                component: Risks
            }

      ]
 
      })
  
 });
