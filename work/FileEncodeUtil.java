package admin;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

//import org.apache.logging.log4j.LogManager;

public class FileEncodeUtil {
//private static org.apache.logging.log4j.Logger logger = LogManager.getLogger(FileEncodeUtil.class.getName());
  public static File cleanFile(String fileName){
	  /*
	   * 先清空文件内容
	   */
	  File file =new File(fileName);
      try {
          if(!file.exists()) {
              file.createNewFile();
          }
          FileWriter fileWriter =new FileWriter(file);
          fileWriter.write("");
          fileWriter.flush();
          fileWriter.close();
      } catch (IOException e) {
          e.printStackTrace();
      }
	return file;
  }
  /**
   * 写入文件
   * 2017年5月8日 下午9:31:13
   * @param file
   * @param str
   * @return
   */
  public static void write(File file,String str){
	  FileOutputStream out = null;
		try {
			 out = new FileOutputStream(file,true);
			 out.write(str.toString().getBytes()); 
			 //out.write("\r\n".getBytes());
			 out.flush();
			 out.close();
			
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
  }

	public static String readtoString(String filePath) {
		StringBuffer sb = new StringBuffer();
		try {
			String encoding = "utf-8";
			File file = new File(filePath);
			if (file.isFile() && file.exists()) { // 判断文件是否存在
				InputStreamReader read = new InputStreamReader(
						new FileInputStream(file), encoding);// 考虑到编码格式
				BufferedReader bufferedReader = new BufferedReader(read);
				String lineTxt = null;
				while ((lineTxt = bufferedReader.readLine()) != null)
					sb.append(lineTxt);
				read.close();
			} else {
//				logger.info("找不到指定的文件");
			}
		} catch (Exception e) {
//			logger.info("读取文件内容出错");
			e.printStackTrace();
		}

		return sb.toString();

	}

public static List<String> read(String filePath){ 
	  /*
	   * 读取文件
	   */
	  List<String> list = new ArrayList<String>();
	//  StringBuffer sb = new StringBuffer();
      try { 
              String encoding="utf-8"; 
              File file=new File(filePath); 
              if(file.isFile() && file.exists()){ //判断文件是否存在 
                  InputStreamReader read = new InputStreamReader( 
                  new FileInputStream(file),encoding);//考虑到编码格式 
                  BufferedReader bufferedReader = new BufferedReader(read); 
                  String lineTxt = null; 
                  while((lineTxt = bufferedReader.readLine()) != null){ 
                	  //System.out.println(lineTxt);
                      //sb.append(lineTxt);
                	  list.add(lineTxt);
                  } 
                  read.close(); 
      }else{ 
//    	  logger.info("找不到指定的文件");
      } 
      } catch (Exception e) { 
//    	  logger.info("读取文件内容出错");
          e.printStackTrace(); 
      }
      //System.out.println(sb.toString());
	return list; 
    
  } 
public static Map<Double,Integer>  readMap(String filePath){
	Map<Double,Integer> map = new HashMap<Double,Integer>();
    try { 
            String encoding="utf-8"; 
            File file=new File(filePath); 
            if(file.isFile() && file.exists()){ //判断文件是否存在 
                InputStreamReader read = new InputStreamReader( 
                new FileInputStream(file),encoding);//考虑到编码格式 
                BufferedReader bufferedReader = new BufferedReader(read); 
                String lineTxt = null;  
                while((lineTxt = bufferedReader.readLine()) != null){ 
                	String[] splits = lineTxt.split("\\s+");
                	double d = Double.parseDouble(splits[1]);
                    if(map.get(d)!=null){
                   	 map.put(d, map.get(d)+1);
                    }else{
                   	 map.put(d, 1);
                    }
                    
                } 
                read.close(); 
    }else{ 
//        logger.info("找不到指定的文件");
    } 
    } catch (Exception e) { 
//        logger.info("读取文件内容出错");
        e.printStackTrace(); 
    }
	return map;
}
public static void readStringDoubleMap(String filePath,Map<String,Double> map){ 
	  /*
	   * 读取文件
	   */
try { 
      String encoding="utf-8"; 
      File file=new File(filePath); 
      if(file.isFile() && file.exists()){ //判断文件是否存在 
          InputStreamReader read = new InputStreamReader( 
          new FileInputStream(file),encoding);//考虑到编码格式 
          BufferedReader bufferedReader = new BufferedReader(read); 
          String lineTxt = null; 
          while((lineTxt = bufferedReader.readLine()) != null){ 
        	  System.out.println(lineTxt);
        	  String[] splits = lineTxt.split("\\s+");
        	  double d = Double.parseDouble(splits[1]);
        	  map.put(splits[0], d);
          } 
          read.close(); 
}else{ 
//  logger.info("找不到指定的文件");
} 
} catch (Exception e) { 
// logger.info("读取文件内容出错");
  e.printStackTrace(); 
}
} 
public static void readStringMap(String filePath,Map<String,String> map){ 
	  /*
	   * 读取文件
	   */
try { 
        String encoding="utf-8"; 
        File file=new File(filePath); 
        if(file.isFile() && file.exists()){ //判断文件是否存在 
            InputStreamReader read = new InputStreamReader( 
            new FileInputStream(file),encoding);//考虑到编码格式 
            BufferedReader bufferedReader = new BufferedReader(read); 
            String lineTxt = null; 
            while((lineTxt = bufferedReader.readLine()) != null){ 
          	  System.out.println(lineTxt);
          	  String[] splits = lineTxt.split("\\s+");
          	  map.put(splits[0], splits[1]);
            } 
            read.close(); 
}else{ 
//    logger.info("找不到指定的文件");
} 
} catch (Exception e) { 
//   logger.info("读取文件内容出错");
    e.printStackTrace(); 
}
} 
}
