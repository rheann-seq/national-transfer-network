// upload.js

$(document).ready(function () {
	function getCookie(name) {
		let cookieValue = null;
		if (document.cookie && document.cookie !== "") {
			const cookies = document.cookie.split(";");
			for (let i = 0; i < cookies.length; i++) {
				const cookie = cookies[i].trim();
				if (cookie.substring(0, name.length + 1) === name + "=") {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}
	const csrftoken = getCookie("csrftoken");

	$("#uploadForm").on("click", function (e) {
		e.preventDefault();

		var formData = new FormData();
		var fileInput = document.getElementById("fileInput");
		var file = fileInput.files[0];
		formData.append("file", file);

		$.ajax({
			url: "http://localhost:8000/api/upload_excel/", // Replace with the actual URL of your ExcelUploadView
			type: "POST",
			data: formData,
			processData: false,
			contentType: false,
			beforeSend: function (xhr, settings) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			},
			success: function (response) {
				console.log("Data uploaded successfully");
				$("#message").html("<p>" + response.message + "</p>");
				$("#fileInput").val("");
			},
			error: function (xhr, status, error) {
				$("#message").html("<p>" + xhr.responseText + "</p>");
			},
		});
	});
});
