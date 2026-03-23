import csv

def save_to_file(file_name, jobs_db):
        # 스크래핑 결과로 CSV파일 생성
    file = open(f"{file_name}.csv","w", encoding="utf-8-sig") #open함수, 파일열기(쓰기모드)
    writer = csv.writer(file) #writer 생성(cvs)
    writer.writerow(["Title","Company","Career", "Reward","Link"]) #List 넘겨줘야함, 헤더작성
    for job in jobs_db: # 헤더에 맞는 데이터 작성(딕셔너리의 values만추출)
        writer.writerow(job.values()) 
    file.close() #파일을 닫아, 다른 곳에서도 사용할 수 있게해줌