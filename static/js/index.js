


async function uploadFile(file){
    let backendResponse = await fetch(`/upload_url`, {
        method : 'POST',
        headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({file_name: file.name, type: file.type})
    })

    if (backendResponse.status != 200){
        alert('error during url request to backend')
        return false
    }

    data = await backendResponse.json()

    const formData = new FormData();
    formData.append('key', file.name);
    formData.append('Content-Type', file.type);
    formData.append('file', file);
  
    let s3Response = await fetch(data.url, {
        method:"POST", 
        body: formData
    })

    if (!s3Response.ok){
        console.log('Error uploading file to s3')
        console.log(s3Response)
        return false
    }
    return true
}


async function submitForm(){
    const leftFile = document.getElementById("left_image").files[0]
    const rightFile = document.getElementById("right_image").files[0]

    if(!leftFile || !rightFile){
        alert('Please select 2 files to stitch')
        return
    }

    if(!uploadFile(leftFile) || !uploadFile(rightFile)){
        alert('error uploading files to s3')
        return
    }

    const data = { left: leftFile.name, right: rightFile.name };

    const resultResponse = await fetch('/result', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
    console.log(resultResponse)
    
    console.log('here 1')
    let resData = await resultResponse.json()
    console.log('resData')
    console.log(resData)

    let resultUrl = resData.image_url;

    let image = document.getElementById("result");
    image.src = resultUrl; // Set the image source to the filename
    console.log(resultUrl)
    image.style.display = "block";
    console.log("DONE")
}