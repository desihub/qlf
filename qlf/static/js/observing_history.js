
$('.input-daterange').datepicker({
    format: "yyyy-mm-dd",
    startDate: "{{ start_date }}",
    endDate: "{{ end_date }}",
    autoclose: true
}).on('changeDate', function(ev){
    console.log('Uau')
});

$('.input-daterange').data("datepicker").pickers[1].setDate("{{ end_date }}");

$(document).ready(function() {
    $('#exposures_table').DataTable( {
        "processing": true,
        "serverSide": true,
        "ajax": $.fn.dataTable.pipeline( {
            "url": "/dashboard/api/datatable_exposures/",
            "pages": 5,
            "type": "GET"
         } ),
         "columns": [
            {"data": "expid"},
            {"data": "tile"},
            {"data": "telra"},
            {"data": "teldec"},
            {"data": "flavor"}
         ]
    } );
} );

/*
$(document).ready(function() {
    $('#example').DataTable( {
        "processing": true,
        "serverSide": true,
        "ajax": $.fn.dataTable.pipeline( {
            url: 'dashboard/',
            pages: 5 // number of pages to cache
        } )
    } );
} );
*/
