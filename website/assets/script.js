function toggleMenu() {
    const nav = document.querySelector('.sidebar');
    nav.style.display = nav.style.display === 'block' ? 'none' : 'block';
}

window.generateLivePDF = function() {
    const cover = document.getElementById('pdf-cover');
    const content = document.getElementById('content');
    
    // Set cover visible for PDF
    cover.style.display = 'block';
    document.getElementById('date-now').textContent = new Date().toLocaleDateString();

    const opt = {
        margin: [10, 15],
        filename: 'OpenClaw-Field-Playbook.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2, useCORS: true },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
    };
    
    html2pdf().set(opt).from(content).save().then(() => {
        cover.style.display = 'none';
    });
};
