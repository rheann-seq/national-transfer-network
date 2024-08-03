
document.getElementById('agreementForm').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent the default form submission
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let universityData=[];

    // First, gather the courses data
    let coursesData = [];
    document.querySelectorAll('#courseTable tbody tr').forEach((row, index) => {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        coursesData.push({
            // cc_name: row.querySelector(`[name="courses[${index}][cc_name]"]`).value,
            course_name: row.querySelector(`[name="courses[${index}][cc_course]"]`).value,
            // effective_term: 'Fall 2021',
            credits: parseInt(row.querySelector(`[name="courses[${index}][cc_credits]"]`).value),
            // university: row.querySelector(`[name="courses[${index}][uc_name]"]`).value,
            uni_course_name: row.querySelector(`[name="courses[${index}][uc_course]"]`).value,
            uni_credits: parseInt(row.querySelector(`[name="courses[${index}][uc_credits]"]`).value, 10),
        });
    });
    try {
        // Post each course to the courses API to get their IDs
        let courseIds = await Promise.all(coursesData.map(async (course) => {
            const response = await fetch(`http://localhost:8000/agreement-courses/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'X-CSRFToken': csrfToken, 
                },
                body: JSON.stringify(course)
            });
            if (!response.ok) {
                throw new Error('Failed to create a course');
            }
            const data = await response.json();
            return data.id;  // Assuming the course creation API returns the new course's ID
        }));

        // Now prepare the agreement data with the course IDs
        const formData = {
            home_institution_name: document.querySelector('[name="home_institution_name"]').value,
            partner_institution_name: document.querySelector('[name="partner_institution_name"]').value,
            program_from_institution_one: document.querySelector('[name="program_from_institution_one"]').value,
            program_at_institution_two: document.querySelector('[name="program_at_institution_two"]').value,
            associate_degree_program: document.querySelector('[name="associate_degree_program"]').value,
            institution_offering_associate_degree: document.querySelector('[name="institution_offering_associate_degree"]').value,
            bachelor_degree_program: document.querySelector('[name="bachelor_degree_program"]').value,
            institution_offering_bachelor_degree: document.querySelector('[name="institution_offering_bachelor_degree"]').value,
            degree_program: document.querySelector('[name="degree_program"]').value,
            field_of_study: document.querySelector('[name="field_of_study"]').value,
            credit_hours: document.querySelector('[name="credit_hours"]').value,
            university_name: document.querySelector('[name="university_name"]').value,
            gpa_requirement: document.querySelector('[name="gpa_requirement"]').value,
            final_degree_program: document.querySelector('[name="final_degree_program"]').value,
            final_institution: document.querySelector('[name="final_institution"]').value,
            courses: courseIds
        };

        // Post the agreement data including course IDs
        const agreementResponse = await fetch(`http://localhost:8000/api/agreements/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-CSRFToken': csrfToken, 
            },
            body: JSON.stringify(formData)
        });

        if (!agreementResponse.ok) {
            throw new Error('Failed to create the agreement');
        }

        const agreementData = await agreementResponse.json();
        console.log('Success:', agreementData);
        alert('Agreement and courses submitted successfully!');
        downloadPDF(agreementData.id);

    } catch (error) {
        console.error('Error:', error);
        alert('Failed to submit the form.');
    }
});

function downloadPDF(agreementId) {
    window.location.href = `http://localhost:8000/api/agreements/pdf/${agreementId}/`;
}
