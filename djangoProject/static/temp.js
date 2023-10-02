// THIS IS THE DISPLAY SCRIPTS

<script>
        let ascendingOrder = true; // Track the current sorting order

        function deleteTask(taskID) {
            fetch('delete-task', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({taskID}),
            })
                .then(response => {
                    // Handle the response here
                    if (response.ok) {
                        console.log('Progress updated successfully.');

                    } else {
                        console.error('Error updating progress.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }

        function toggleOrder() {
            var table = document.getElementById('taskTable');
            var rows = Array.from(table.querySelectorAll('tr[data-progress]'));
            rows.sort(function (a, b) {
                var progressOrder = ['TODO', 'INPROGRESS', 'REVIEW', 'DONE'];
                var progressA = a.getAttribute('data-progress');
                var progressB = b.getAttribute('data-progress');

                // Toggle the sorting order
                if (ascendingOrder) {
                    return progressOrder.indexOf(progressA) - progressOrder.indexOf(progressB);
                } else {
                    return progressOrder.indexOf(progressB) - progressOrder.indexOf(progressA);
                }
            });
            rows.forEach(function (row) {
                table.appendChild(row);
            });

            // Toggle the sorting order variable
            ascendingOrder = !ascendingOrder;
        }

        function updateProgress(selectElement, taskId) {
            // Get the selected value from the dropdown
            var newProgress = selectElement.value;

            // Use AJAX (or fetch) to send a POST request to update the task's progress
            // Replace this with your actual POST request code
            // Example using fetch:
            fetch('update-progress', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({taskId, newProgress}),
            })
                .then(response => {
                    // Handle the response here
                    if (response.ok) {
                        console.log('Progress updated successfully.');

                    } else {
                        console.error('Error updating progress.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
    </script>