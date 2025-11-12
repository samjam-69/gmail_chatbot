from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from test2 import bod_met
from langchain_core.documents import Document
load_dotenv()
model=ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")
def conv(num):
    g_mail=bod_met(num)
    doc_lst=[]
    for message in g_mail:
        #"From":sender,"Subject":subject,"Date":date,'id':msg['id'],'body':body}
        
        result=model.invoke("convert this mail to text message removing html commands /n "+message["body"])
        new_result=model.invoke("Summarize this mail in less than 100 words"+result.content)
        doc=Document(
            page_content=new_result.content,
            metadata={"from":message["From"],"subject":message["Subject"],"date":message["Date"]},
            id=message["id"]
        )
        doc_lst.append(doc)
    return doc_lst
if __name__=="__main__":
    print(conv(10))