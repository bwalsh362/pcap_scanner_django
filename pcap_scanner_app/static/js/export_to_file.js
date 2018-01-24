$(document).ready(function() {
    $('table').each(function () {
        var $table = $(this);

        var $button = $("<button type='button' class='btn btn-default'>");
        $button.text("Export Table to CSV");
        $button.insertAfter($table);

        $button.click(function () {
            var csv = $table.table2CSV({
                delivery: 'value'
            });
            window.location.href = 'data:text/csv,'
            + encodeURIComponent(csv);

        });
    });
});
