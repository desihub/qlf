Ext.application({
    name: 'Supervisor',


    launch : function() {
       Ext.create('Ext.panel.Panel', {
          title: 'Extjs',
          width: 700,
          height: 700,
          items:[{
            xtype: 'container',
            listeners : {
              'afterrender': function(a){
                console.log(a.id)
                Ext.Ajax.request({
                  url: '/dashboard/api/bokeh/',
                  success: function(response){
                    var obj = Ext.decode(response.responseText);
                    console.log(obj[0].links.src)
                    console.log(obj[0].links.id)
                    var imported = document.createElement('script');
                    imported.src = obj[0].links.src;
                    imported.id = obj[0].links.id;
                    document.getElementById(a.id).style.height = "650px"
                    document.getElementById(a.id).appendChild(imported)
                  }
                })
              }
            },
          }],
          renderTo: Ext.getBody()
      });
      //win.show();
    },
  
});

