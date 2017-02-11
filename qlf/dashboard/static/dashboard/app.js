Ext.application({
    name: 'Supervisor',


    launch : function() {
       var win = Ext.create("Ext.window.Window", {
           title: 'My first window',
           width: 300,
           height: 200,
           maximizable: true,
           html: 'this is my first window'
       });
       win.show();
    }
});
