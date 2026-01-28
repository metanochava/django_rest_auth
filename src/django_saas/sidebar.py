
MENU = "Core"
ICON = "menu"


 
SUBMENUS = [
    {
        "menu": "Dashboard",
        "icon": "dashboard",
        "role": "view_django_saas_dashboard",
        "rota": "view_django_saas_dashboard",
    },
    {
        "menu": "TipoEntidade",
        "icon": "corporate_fare",
        "role": "list_tipoentidade",
        "rota": "list_tipoentidade",
        "add_role": "add_tipoentidade",
        "add_rota": "add_tipoentidade",
    },    
    {
        "menu": "Entidades",
        "icon": "home",
        "role": "list_entidade",
        "rota": "list_entidade",
        "submenu": [
            {
                "menu": "Entidades",
                "icon": "home",
                "role": "list_entidade",
                "rota": "list_entidade",
                "add_role": "add_tipoentidad",
                "add_rota": "add_tipoentidade",
            },
            {
                "menu": "Entidades",
                "icon": "home",
                "role": "list_entidade",
                "rota": "list_entidade",
            }
        ]
    },  
     
    {
        "menu": "Entidade",
        "icon": "home",
        "role": "view_entidade",
        "rota": "view_entidade",
    },  
    {
        "menu": "Sucursal",
        "icon": "house",
        "role": "list_sucursal",
        "rota": "list_sucursal",
    }, 
    {
        "menu": "Grupos",
        "icon": "groups",
        "role": "list_group",
        "rota": "list_group",
    }, 
    {
        "menu": "Users",
        "icon": "face",
        "role": "list_user",
        "rota": "list_user",
    },{
        "menu": "UserAll",
        "icon": "people",
        "role": "list_user_all",
        "rota": "list_userall",
    },  
    {
        "menu": "Inputs",
        "icon": "input",
        "role": "list_input",
        "rota": "list_input",
    }, 
    {
        "menu": "Cometario",
        "icon": "mode_comment",
        "role": "list_cometario",
        "rota": "list_cometario",
        
    }, 
    
]