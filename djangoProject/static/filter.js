<script src="jquery-3.7.1.min.js"></script>
<script>
$(document).ready(function() {
  $('#user-filter-form input').on('input', function() {
    // Get filter values from input fields
    var employeeNumber = $('#filter-employee-number').val();
    var firstName = $('#filter-first-name').val();
    var secondName = $('#filter-second-name').val();
    var alias = $('#filter-alias').val();
    var startDate = $('#filter-start-date').val();

    // Send AJAX request to the filter_users view
    $.ajax({
      url: '/filter_users/',
      type: 'GET',
      data: {
        employee_number: employeeNumber,
        first_name: firstName,
        second_name: secondName,
        alias: alias,
        start_date: startDate,
      },
      dataType: 'json',
      success: function(data) {
        // Clear the table body
        $('#user-table tbody').empty();

        // Populate the table with filtered data
        data.filtered_users.forEach(function(user) {
          $('#user-table tbody').append(
            '<tr>' +
            '<td>' + user.employee_number + '</td>' +
            '<td>' + user.first_name + '</td>' +
            '<td>' + user.second_name + '</td>' +
            '<td>' + user.alias + '</td>' +
            '<td>' + user.start_date + '</td>' +
            '</tr>'
          );
        });
      },
      error: function(xhr, status, error) {
        console.error(error)
      }
    })
  })
})
</script>
