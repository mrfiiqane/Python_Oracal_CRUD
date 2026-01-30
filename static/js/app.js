$(document).ready(function() {
    // API Basic URL
    const API_URL = '/api/students';

    // Load students on startup
    loadStudents();

    // Show modal
    $('#btnAddNew').click(function() {
        resetForm();
        $('#modalTitle').text('Add New Student');
        showModal();
    });

    // Close modal
    $('#btnCloseModal, #btnCancel').click(function() {
        hideModal();
    });

    // Handle Form Submit (Add/Update)
    $('#studentForm').submit(function(e) {
        e.preventDefault();
        
        const id = $('#studentId').val();
        const data = {
            name: $('#name').val(),
            email: $('#email').val(),
            course: $('#course').val()
        };

        if (id) {
            // Update
            updateStudent(id, data);
        } else {
            // Add
            addStudent(data);
        }
    });

    // Functions
    function loadStudents() {
        $.ajax({
            url: API_URL,
            method: 'GET',
            success: function(students) {
                let html = '';
                if (students.length === 0) {
                    html = `<tr><td colspan="5" class="px-6 py-12 text-center text-slate-400">No students found. Add one to get started!</td></tr>`;
                } else {
                    students.forEach(student => {
                        html += `
                            <tr class="hover:bg-slate-50/80 transition-all">
                                <td class="px-6 py-4 text-sm text-slate-500 font-mono">#${student.id}</td>
                                <td class="px-6 py-4">
                                    <span class="text-sm font-semibold text-slate-800">${student.name}</span>
                                </td>
                                <td class="px-6 py-4 text-sm text-slate-600">${student.email}</td>
                                <td class="px-6 py-4">
                                    <span class="px-3 py-1 bg-indigo-50 text-indigo-600 rounded-full text-xs font-semibold">${student.course || 'N/A'}</span>
                                </td>
                                <td class="px-6 py-4 text-right space-x-2">
                                    <button onclick="editStudent(${student.id}, '${student.name}', '${student.email}', '${student.course}')" class="p-2 text-slate-400 hover:text-indigo-600 transition-all">
                                        <i class="fas fa-edit"></i>
                                    </button>
                                    <button onclick="deleteStudent(${student.id})" class="p-2 text-slate-400 hover:text-rose-600 transition-all">
                                        <i class="fas fa-trash"></i>
                                    </button>
                                </td>
                            </tr>
                        `;
                    });
                }
                $('#studentTableBody').html(html);
                $('#totalCount').text(students.length);
            },
            error: function(err) {
                showToast('Error loading students: ' + (err.responseJSON?.error || 'Unknown error'), 'error');
            }
        });
    }

    function addStudent(data) {
        $.ajax({
            url: API_URL,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function() {
                showToast('Student added successfully!');
                hideModal();
                loadStudents();
            },
            error: function(err) {
                showToast(err.responseJSON?.error || 'Failed to add student', 'error');
            }
        });
    }

    function updateStudent(id, data) {
        $.ajax({
            url: `${API_URL}/${id}`,
            method: 'PUT',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function() {
                showToast('Student updated successfully!');
                hideModal();
                loadStudents();
            },
            error: function(err) {
                showToast(err.responseJSON?.error || 'Failed to update student', 'error');
            }
        });
    }

    window.deleteStudent = function(id) {
        if (confirm('Are you sure you want to delete this student?')) {
            $.ajax({
                url: `${API_URL}/${id}`,
                method: 'DELETE',
                success: function() {
                    showToast('Student deleted successfully!');
                    loadStudents();
                },
                error: function(err) {
                    showToast(err.responseJSON?.error || 'Failed to delete student', 'error');
                }
            });
        }
    };

    window.editStudent = function(id, name, email, course) {
        $('#studentId').val(id);
        $('#name').val(name);
        $('#email').val(email);
        $('#course').val(course !== 'null' ? course : '');
        $('#modalTitle').text('Edit Student');
        showModal();
    };

    function showModal() {
        $('#studentModal').removeClass('opacity-0 pointer-events-none');
        $('#studentModal > div').removeClass('scale-95').addClass('scale-100');
    }

    function hideModal() {
        $('#studentModal').addClass('opacity-0 pointer-events-none');
        $('#studentModal > div').removeClass('scale-100').addClass('scale-95');
    }

    function resetForm() {
        $('#studentId').val('');
        $('#studentForm')[0].reset();
    }

    function showToast(message, type = 'success') {
        const toast = $('#toast');
        const icon = $('#toastIcon');
        
        $('#toastMessage').text(message);
        
        if (type === 'error') {
            toast.removeClass('bg-slate-800').addClass('bg-rose-600');
            icon.removeClass('text-emerald-400 text-amber-400').addClass('text-white');
        } else {
            toast.removeClass('bg-rose-600').addClass('bg-slate-800');
            icon.addClass('text-emerald-400');
        }

        toast.removeClass('translate-y-20 opacity-0').addClass('translate-y-0 opacity-100');
        
        setTimeout(() => {
            toast.addClass('translate-y-20 opacity-0').removeClass('translate-y-0 opacity-100');
        }, 3000);
    }
});
