import os

import gradio as gr
import tempfile
import shutil
def generate_file(file_obj):
    global tmpdir
    print('临时文件夹地址：{}'.format(tmpdir))
    print('上传文件的地址：{}'.format(file_obj.name)) # 输出上传后的文件在gradio中保存的绝对地址

    shutil.copy(file_obj.name, tmpdir)

    # 获取上传Gradio的文件名称
    FileName=os.path.basename(file_obj.name)

    # 获取拷贝在临时目录的新的文件地址
    NewfilePath=os.path.join(tmpdir,FileName)
    print(NewfilePath)

    # 打开复制到新路径后的文件
    with open(NewfilePath, 'rb') as file_obj:

        #在本地电脑打开一个新的文件，并且将上传文件内容写入到新文件
        outputPath=os.path.join(tmpdir,"New"+FileName)
        with open(outputPath,'wb') as w:
            w.write(file_obj.read())

    # 返回新文件的的地址（注意这里）
    return outputPath
def main():
    global tmpdir
    with tempfile.TemporaryDirectory(dir='.') as tmpdir:
        # 定义输入和输出
        inputs = [
            gr.Dropdown(
                choices=["huawei", "tianshu", "hanwuji"],value="huawei", multiselect=False, label="GPU", info="选择国产显卡."
        ),
            gr.components.File(label="上传文件")
        ]
        outputs = gr.components.File(label="下载文件")

        # 创建 Gradio 应用程序
        huawei = gr.Interface(fn=generate_file, inputs=inputs, outputs=outputs,   title="模型实现代码转换(based on QWen LLM)",
                      description="支持上传模型实现的.py文件、txt文件"
      )
        tianshu = gr.Interface(lambda name: "Bye " + name, "text", "text")
        
        app=gr.TabbedInterface([huawei, tianshu], ["模型代码适配", "推理性能展示"])

        # 启动应用程序
        app.launch(share=True)
if __name__=="__main__":
    main()
