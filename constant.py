import os
import shutil

secrete_message_dir_path = "./1-Secre"
mines_lacate_dir_path = "./2-Locat"
marked_image_dir_path = "./3-Marke"
embeded_message_dir_path = "./4-Embed"
recognized_image_dir_path = "./5-Recog"
extract_message_dir_path = "./6-Extra"
entropy_result_dir_path = "./7-Entro"

runner_image_dir_path = "./Mark_pic"


def clear_folder(folder_path):
    """
    清空指定資料夾中的所有檔案和子目錄。

    :param folder_path: 資料夾的路徑
    """
    if not os.path.exists(folder_path):
        print(f"資料夾 {folder_path} 不存在！")
        return

    # 遍歷資料夾內容
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                # 刪除檔案或符號連結
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                # 刪除子目錄
                shutil.rmtree(item_path)
        except Exception as e:
            print(f"無法刪除 {item_path}，原因：{e}")


if __name__ == "__main__":
    clear_folder(mines_lacate_dir_path)
    clear_folder(marked_image_dir_path)
    clear_folder(embeded_message_dir_path)
    clear_folder(recognized_image_dir_path)
    clear_folder(extract_message_dir_path)
    clear_folder(runner_image_dir_path)