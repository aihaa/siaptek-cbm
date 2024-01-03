from plyer import notification

def desk_notification(data_point, threshold):
    notification.notify(
            title = "ALERT!!",
            message=f"Hi Mr. Arif, data point {data_point} is exceeding threshold {threshold} on engine M45R." ,
           
            # displaying time
            timeout=2
)
    