function updateFileName(input, spanId) {
    const fileName = input.files[0] ? input.files[0].name : 'Seleccionar archivo';
    document.getElementById(spanId).textContent = fileName;
}

//modal
document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");

    form.addEventListener("submit", function (event) {
        
        const modal = document.getElementById("modal");
        modal.style.display = "block";
        
        const modalMessage = document.getElementById("modalMessage");
        modalMessage.innerText = "Generando archivo...";

        setTimeout(() => {
            modalMessage.innerText = "Asignaciones generadas correctamente";
            document.getElementById("downloadBtn").style.display = "inline-block";
            document.getElementById("downloadBtnPDF").style.display = "inline-block";
        }, 3000); 
    });

    window.onclick = function (event) {
        const modal = document.getElementById("modal");
        if (event.target === modal) {
            closeModal();
        }
    };
});

function downloadFile() {
    const downloadUrl = `/download/asignaciones_resultado.csv`; 
    const link = document.createElement('a');
    link.href = downloadUrl; 
    link.download = 'asignaciones_resultado.csv'; 
    document.body.appendChild(link);
    link.click(); 
    document.body.removeChild(link); 
    //closeModal(); 
}

function downloadFilePDF() {
    const downloadUrl = `/download/asignaciones_visual.pdf`; 
    const link = document.createElement('a');
    link.href = downloadUrl; 
    link.download = 'asignaciones_visual.pdf'; 
    document.body.appendChild(link);
    link.click(); 
    document.body.removeChild(link); 
    //closeModal(); 
}

function closeModal() {
    const modal = document.getElementById("modal");
    modal.style.display = "none";
    document.getElementById("downloadBtn").style.display = "none";
}

//
function openHelpClasses() {
    document.getElementById("helpModalClasses").style.display = "flex";
}

function openHelpRooms(){
    document.getElementById("helpModalRooms").style.display = "flex";
}

function closeModalClasses() {
    document.getElementById("helpModalClasses").style.display = "none";
}

function closeModalRooms() {
    document.getElementById("helpModalRooms").style.display = "none";
}

window.onclick = function(event) {
    var modalRooms = document.getElementById("helpModalRooms");
    var modalClasses = document.getElementById("helpModalClasses");
    if (event.target === (modalClasses && modalRooms)) {
        closeModal();
    }
}



