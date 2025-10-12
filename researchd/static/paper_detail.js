// PDF.js viewer functionality
// Get PDF URL from data attribute

let pdfDoc = null,
    pageNum = 1,
    pageRendering = false,
    pageNumPending = null,
    scale = 1,
    canvas = document.getElementById('pdf-canvas'),
    ctx = canvas.getContext('2d');

// Get PDF URL from the pdf-viewer data attribute
const pdfViewer = document.getElementById('pdf-viewer');
const pdfUrl = pdfViewer ? pdfViewer.getAttribute('data-pdf-url') : null;

function renderPage(num) {
    pageRendering = true;
        pdfDoc.getPage(num).then(function(page) {
            const container = document.getElementById("pdf-viewer");

            // Unscaled viewport
            const unscaledViewport = page.getViewport({ scale: 1 });

            // Fit-to-width scale
            const desiredWidth = container.clientWidth;
            scale = desiredWidth / unscaledViewport.width;

            // Retina/HiDPI support
            const outputScale = window.devicePixelRatio || 1;
            const viewport = page.getViewport({ scale: scale });

            canvas.width = Math.floor(viewport.width * outputScale);
            canvas.height = Math.floor(viewport.height * outputScale);
            canvas.style.width = "100%";
            canvas.style.height = "auto";

            const transform = outputScale !== 1
                ? [outputScale, 0, 0, outputScale, 0, 0]
                : null;

            const renderContext = {
                canvasContext: ctx,
                viewport: viewport,
                transform: transform
            };

            const renderTask = page.render(renderContext);
            renderTask.promise.then(function() {
                pageRendering = false;
                if (pageNumPending !== null) {
                    renderPage(pageNumPending);
                    pageNumPending = null;
                    }
            });
        });

    document.getElementById('page_num').textContent = num;
}

function queueRenderPage(num) {
    if (pageRendering) {
        pageNumPending = num;
    } else {
        renderPage(num);
    }
}

function onPrevPage() {
    if (pageNum <= 1) return;
    pageNum--;
    queueRenderPage(pageNum);
}

function onNextPage() {
    if (pageNum >= pdfDoc.numPages) return;
    pageNum++;
    queueRenderPage(pageNum);
}

function zoomIn() {
    scale += 0.2;
    queueRenderPage(pageNum);
}

function zoomOut() {
    if (scale > 0.4) {
        scale -= 0.2;
        queueRenderPage(pageNum);
    }
}

document.getElementById('prev').addEventListener('click', onPrevPage);
document.getElementById('next').addEventListener('click', onNextPage);
document.getElementById('zoom_in').addEventListener('click', zoomIn);
document.getElementById('zoom_out').addEventListener('click', zoomOut);

// Load the PDF from data attribute
if (pdfUrl) {
    pdfjsLib.getDocument(pdfUrl).promise.then(function(pdfDoc_) {
        pdfDoc = pdfDoc_;
        document.getElementById('page_count').textContent = pdfDoc.numPages;
        renderPage(pageNum);
    });
}

// Re-render on window resize (keep fit-to-width)
window.addEventListener("resize", () => {
    queueRenderPage(pageNum);
});

