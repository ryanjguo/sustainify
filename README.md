# sustainify 🌏

### Inspiration 💡
Every year, not only Canadians but people around the world are throwing too much garbage into the wrong bins. Specifically, too much garbage is being thrown into our precious recycling bins. Infact, according to a CBC article, nearly 1 in every 3 pounds are not supposed to be there. This causes contamination and hundreds of cities around the world are struggling with this problem. So that's where we as a team, Daniel, Ryan, and Sahith came up with our product, ‘sustainify’. 

### What It Does 🛠️
sustainify is a web application designed to promote sustainable living by providing real-time, personalised waste disposal instructions. Users can either upload a picture of their waste item or use their webcam to capture an image. sustainify, which is powered by a pre-trained AI model, identifies the waste and provides detailed, tailored instructions on how to dispose of it properly, promoting recycling and proper waste management. sustainify is user-friendly, with a simple and intuitive interface ensuring ease of use for individuals of all ages. sustainify is not just a tool but an educational resource, raising awareness about the environmental impacts of waste and encouraging a culture of responsibility and sustainability to people of all ages, from school students to elderly citizens.

### How We Built It 👷
For this project, we used Flask, as well as HTML, CSS, and JS, to create the website. We used Python for a lot of the backend integration, including manipulating the images, and calling the APIs. We used a pre-trained model for our image detection due to the lack of time and since training our own would require many resources that we don’t possess. Once we identified the material, we passed that material into a prompt we engineered into the OpenAI API, which gets a response from a gpt-3.5 model to give users advice on how to properly dispose of this object, as well as possible side effects when that object is improperly disposed of.

### Moving Forward... 🔜
1) **Training our own AI model instead of using a pre-trained model;** this will not only provide us with deeper knowledge of AI, but also may improve accuracy and expand the scope of objects **sustainify** will be able to classify
2) **Mobile version of app to improve accessibility;** Creating a mobile app for **sustainify** will greatly improve usability, as most users will be on mobile devices 
3) **Improve performance;** **sustainify** currently tends to be slow, and the pretrained model limits both its' accuracy and speed. We wish to focus on improving both, bringing users a more reliable and enjoyable experience
4) **Having 2 sections when displaying results:**
          * Section that only states which bin to use
          * Section that displays the full description on proper waste disposal
  Some users don't care about the explanation, they just want to know which bin to throw it in. This will allow them to quickly dispose of their item, with an optional explanation if they wish to further educate           themselves.



