Ext.onReady(function() {  
  Ext.tip.QuickTipManager.init();
  
  //-------------- container with bokeh ---------------
  var panelBokeh = {
        title: 'QA',
        iconCls: 'x-fa fa-line-chart',
        height: 1024,
        items:[{
        xtype: 'panel',        
        width: 650,
        
        items:[{
            xtype: 'component',
            html: '<h2>Spectral signal-to-noise</h2><br>Calculation of the spectral signal-to-noise  after sky subtraction.',
        },
        {
            buttonAlign: 'right',
            margin: '10 0 0 0',
            buttons: [{
                 xtype: 'button',
                 formBind: true,
                 itemId: 'btnLogin',
                 text: 'SEE MORE',
                  handler: function(button) {
                    setBokeh(button)
                  },
            }]
        },{
            xtype: 'component',
            id: 'test_compapp',
            width: 650,
            text: 'test'
            // height: 650           
        }]  
  
    },
    {
        xtype: 'panel',        
        width: 650,
        items:[{
            xtype: 'component',
            html: '<h2>Et harum quidem rerum facilis</h2><br>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        },
        {
            buttonAlign: 'right',
            buttons: [{
                 xtype: 'button',
                 formBind: true,
                 itemId: 'btnLogin',
                 text: 'READ MORE',
            }]
        }]
    }]
    }
  //-------------- container with bokeh ---------------


  //-------------- MAIN PANEL ---------------
  var mainPanel = Ext.create('Ext.tab.Panel', {
    titleRotation: 0,
    tabRotation: 0,
    title: 'Quick Look',
    iconCls: 'x-fa fa-th-list',
    items: [{
        title: 'Home',
        iconCls: 'x-fa fa-home',
        //listeners: {
        //    afterrender: 'teste'
        //}
    },{
        title: 'Configuration',
        iconCls: 'x-fa fa-cog',
        width: 500,
        // height: 400,        
        // layout: {
        //     type: 'hbox',
        //     pack: 'start',
        //     // align: 'stretch'
        // },
        // The following grid shares a store with the classic version's grid as well!
        items: [{
            flex: 1,     
            // xtype: 'mainlist',
            // title: ' &nbsp',
            margin: '0 10 0 0'
        }]
    }, {
        title: 'Monitor',
        iconCls: 'x-fa fa-desktop',
        // xtype: 'ccd'
    },panelBokeh 
    ],
    renderTo: Ext.getBody(),
  });  
  //-------------- MAIN PANEL ---------------

  //-------------- functions ---------------

  function setBokeh(el){
    Ext.Ajax.request({
      url: '/dashboard/api/bokeh/',
      success: function(response){
        var obj = Ext.decode(response.responseText);
        if (el.text == 'SEE MINUS'){
            document.getElementById('test_compapp').innerHTML = ""
            document.getElementById("test_compapp").style.height = "0px"
            el.setText('SEE MORE')
        }else{
            var imported = document.createElement('script');
            imported.src = obj[0].links.src;
            imported.id = obj[0].links.id;
            document.getElementById("test_compapp").style.height = "650px"
            document.getElementById('test_compapp').appendChild(imported)
            el.setText('SEE MINUS')
        }
      }
    })
  }
});